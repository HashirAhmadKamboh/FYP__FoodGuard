from pydantic import BaseModel, ConfigDict
from typing import Optional

class NutritionalProfileOut(BaseModel):
    id: int
    energy_kcal: Optional[float]
    protein_g: Optional[float]
    fat_g: Optional[float]
    carbs_g: Optional[float]
    fiber_g: Optional[float]
    water_pct: Optional[str]
    vitamins_minerals: Optional[str]
    phytochemicals: Optional[str]
    serving_size: Optional[str]

    model_config = ConfigDict(from_attributes=True)

class CommodityOut(BaseModel):
    id: int
    name: str
    category: str
    nutrition: Optional[NutritionalProfileOut] = None

    model_config = ConfigDict(from_attributes=True)