from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Request, Depends
from typing import Optional, List
from app.db.session import SessionDep
from app.account.dependencies import get_current_user, get_optional_current_user
from app.account.models import User
from .schemas import PredictRequest, PredictionResultOut, PredictionHistoryOut
from . import services

router = APIRouter(prefix="/predict", tags=["AI Prediction"])

@router.get("/history")
async def get_prediction_history(
    session: SessionDep,
    current_user: User = Depends(get_current_user)
):
    return await services.get_user_prediction_history(session, current_user)

@router.post("/")
async def predict_food(
    session: SessionDep,
    request: Request,
    file: Optional[UploadFile] = File(None),
    city: Optional[str] = Form("lahore"), # Default to lahore if not provided
    current_user: Optional[User] = Depends(get_optional_current_user)
):
    # 1. AI PREDICTION
    if file is None:
        # Fallback for React Native FormData issues
        form_data = await request.form()
        file_part = form_data.get("file")
        if file_part is None:
            raise HTTPException(status_code=400, detail="No file provided in the request")
        
        if hasattr(file_part, "read"):
            img_bytes = await file_part.read()
        elif isinstance(file_part, str):
            import base64
            try:
                if "," in file_part:
                    file_part = file_part.split(",")[1]
                img_bytes = base64.b64decode(file_part)
            except:
                img_bytes = file_part.encode('utf-8')
        else:
            img_bytes = file_part
            
        city_form = form_data.get("city")
        if city_form:
            city = city_form
    else:
        img_bytes = await file.read()

    return await services.process_prediction(img_bytes, city, session, current_user)

@router.post("/base64")
async def predict_food_base64(
    req: PredictRequest,
    session: SessionDep,
    current_user: Optional[User] = Depends(get_optional_current_user)
):
    import base64
    try:
        base64_str = req.file_base64
        if "," in base64_str:
            base64_str = base64_str.split(",")[1]
        img_bytes = base64.b64decode(base64_str)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid base64 encoding")
    
    return await services.process_prediction(img_bytes, req.city, session, current_user)