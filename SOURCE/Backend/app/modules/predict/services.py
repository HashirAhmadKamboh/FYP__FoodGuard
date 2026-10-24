import os
import uuid
from typing import Optional, List, Dict, Any
from fastapi import HTTPException
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy import desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.ml_predictor import ml_model
from app.modules.commodities.models import Commodity
from app.modules.prices.models import PriceRecord
from app.account.models import User, PredictionHistory

# Mappings for database Commodity table lookup (Nutritional info)
COMMODITY_MAPPING = {
    "Meat": "Meat (Beef)",
    "Potato": "Potato / Aloo",
    "Tomato": "Tomato / Tamatar",
    "Okra": "Okra / Bhindi",
    "Cucumber": "Cucumber / Kheera",
    "Carrot": "Carrot / Gajar",
    "Bittergourd": "Bitter Gourd / Karela",
    "Bitter Gourd": "Bitter Gourd / Karela",
    "Bellpepper": "Bell Pepper / Shimla Mirch",
    "Bell Pepper": "Bell Pepper / Shimla Mirch",
    "Capsicum": "Capsicum / Shimla Mirch",
}

# Mappings for PriceRecord table lookup (Local rates)
PRICE_SEARCH_MAPPING = {
    "Bittergourd": "Bitter Gourd",
    "Bellpepper": "Capsicum",
    "Orange": "Kinnow",
    "Grape": "Grapes",
}

async def process_prediction(
    img_bytes: bytes,
    city: str,
    session: AsyncSession,
    current_user: Optional[User] = None
) -> Dict[str, Any]:
    try:
        prediction = ml_model.predict(img_bytes)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid image format. Could not process the file. Error: {str(e)}"
        )
        
    detected_item = prediction["item"]
    is_food = prediction.get("is_food", True)
    
    if not is_food:
        result_payload = {
            "ai_prediction": prediction,
            "nutritional_info": "Not applicable for non-food items.",
            "district_pricing": []
        }
    else:
        # 2. GET NUTRITIONAL DATA
        commodity_query_name = COMMODITY_MAPPING.get(detected_item, detected_item)
        result = await session.execute(
            select(Commodity)
            .options(selectinload(Commodity.nutrition))
            .where(Commodity.name == commodity_query_name)
        )
        commodity = result.scalar_one_or_none()
        
        if not commodity:
            # Fallback to case-insensitive partial match (safe against multiple hits via .first())
            result = await session.execute(
                select(Commodity)
                .options(selectinload(Commodity.nutrition))
                .where(Commodity.name.ilike(f"%{commodity_query_name}%"))
            )
            commodity = result.scalars().first()
        
        # 3. GET PRICE DATA FOR DISTRICT
        price_search_name = PRICE_SEARCH_MAPPING.get(detected_item, detected_item)
        price_result = await session.execute(
            select(PriceRecord)
            .where(PriceRecord.city_name == city.lower())
            .where(PriceRecord.item_name.ilike(f"%{price_search_name}%"))
            .order_by(desc(PriceRecord.scrape_date))
        )
        records = price_result.scalars().all()
        
        if records:
            latest_date = records[0].scrape_date
            latest_records = [r for r in records if r.scrape_date == latest_date]
        else:
            latest_records = []
        
        # Format nutritional info
        nutritional_info = commodity.nutrition if commodity else "Nutrition data pending."

        result_payload = {
            "ai_prediction": prediction,
            "nutritional_info": nutritional_info,
            "district_pricing": [
                {
                    "city": city,
                    "item_name": r.item_name,
                    "min_price": r.min_price,
                    "max_price": r.max_price,
                    "dc_price": r.dc_price,
                    "psba_price": r.psba_price,
                    "source": r.source,
                } for r in latest_records
            ]
        }

    # If the user is logged in, save the prediction history
    if current_user:
        # Save image file to static folder
        image_filename = f"{uuid.uuid4()}.jpg"
        image_dir = "static/predictions"
        os.makedirs(image_dir, exist_ok=True)
        image_path = os.path.join(image_dir, image_filename)
        
        try:
            with open(image_path, "wb") as f:
                f.write(img_bytes)
        except Exception as e:
            print(f"⚠️ Failed to save prediction image to disk: {e}")
            image_path = None
        
        # Format nutritional data
        nutrition_db = None
        if is_food and commodity and commodity.nutrition:
            nutrition_db = {
                "energy_kcal": commodity.nutrition.energy_kcal,
                "protein_g": commodity.nutrition.protein_g,
                "fat_g": commodity.nutrition.fat_g,
                "carbs_g": commodity.nutrition.carbs_g,
                "fiber_g": commodity.nutrition.fiber_g,
                "water_pct": commodity.nutrition.water_pct,
                "vitamins_minerals": commodity.nutrition.vitamins_minerals,
                "phytochemicals": commodity.nutrition.phytochemicals,
                "serving_size": commodity.nutrition.serving_size
            }
            
        history_record = PredictionHistory(
            user_id=current_user.id,
            image_path=image_path,
            item=detected_item,
            confidence=float(prediction.get("item_confidence", 0.0)),
            freshness=prediction.get("freshness", "Unknown"),
            is_food=is_food,
            city=city,
            nutritional_info=nutrition_db,
            district_pricing=result_payload["district_pricing"]
        )
        session.add(history_record)
        await session.commit()
        result_payload["saved_to_history"] = True
        
    return result_payload

async def get_user_prediction_history(
    session: AsyncSession,
    current_user: User
) -> List[Dict[str, Any]]:
    stmt = (
        select(PredictionHistory)
        .where(PredictionHistory.user_id == current_user.id)
        .order_by(desc(PredictionHistory.created_at))
    )
    result = await session.execute(stmt)
    history = result.scalars().all()
    
    return [
        {
            "id": h.id,
            "item": h.item,
            "confidence": h.confidence,
            "freshness": h.freshness,
            "is_food": h.is_food,
            "city": h.city,
            "created_at": h.created_at.isoformat(),
            "image_url": f"/static/predictions/{os.path.basename(h.image_path)}" if h.image_path else None,
            "nutritional_info": h.nutritional_info,
            "district_pricing": h.district_pricing
        } for h in history
    ]
