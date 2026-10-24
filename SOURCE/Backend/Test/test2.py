import asyncio
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import AsyncSessionLocal
from app.modules.commodities.models import Commodity
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from fastapi.encoders import jsonable_encoder

async def main():
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Commodity).options(selectinload(Commodity.nutrition)).limit(1))
        commodity = result.scalar_one_or_none()
        
        response_data = {
            "ai_prediction": {"item": "Apple", "freshness": "fresh", "confidence": "98%"},
            "nutritional_info": commodity.nutrition if commodity else "Nutrition data pending.",
            "district_pricing": [
                {
                    "city": "lahore",
                    "item_name": "Apple",
                    "min_price": 100,
                    "max_price": 120,
                    "dc_price": 110,
                    "psba_price": 115,
                    "source": "amisprizescrape",
                }
            ]
        }
        try:
            print(jsonable_encoder(response_data))
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
