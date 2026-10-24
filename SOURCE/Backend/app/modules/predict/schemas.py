from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Any

class PredictRequest(BaseModel):
    file_base64: str
    city: str = "lahore"

class DistrictPricingOut(BaseModel):
    city: str
    item_name: str
    min_price: Optional[float]
    max_price: Optional[float]
    dc_price: Optional[float]
    psba_price: Optional[float]
    source: Optional[str]

class PredictionResultOut(BaseModel):
    ai_prediction: Any
    nutritional_info: Any  # Can be dict, string, or NutritionalProfile object
    district_pricing: List[DistrictPricingOut]
    saved_to_history: Optional[bool] = None

class PredictionHistoryOut(BaseModel):
    id: int
    item: str
    confidence: float
    freshness: str
    is_food: bool
    city: str
    created_at: str
    image_url: Optional[str]
    nutritional_info: Optional[Any]
    district_pricing: Optional[List[DistrictPricingOut]]

    model_config = ConfigDict(from_attributes=True)
