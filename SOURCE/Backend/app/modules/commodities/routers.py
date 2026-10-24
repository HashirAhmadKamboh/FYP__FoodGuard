from fastapi import APIRouter
from typing import List
from app.db.session import SessionDep
from .schemas import CommodityOut
from . import services

router = APIRouter(prefix="/api/commodities", tags=["Commodities"])

@router.get("/", response_model=List[CommodityOut])
async def get_all_ingredients(session: SessionDep):
    """Get all food items and their nutritional profiles."""
    return await services.get_all_commodities(session)

@router.get("/{name}", response_model=CommodityOut)
async def get_ingredient(session: SessionDep, name: str):
    """Get specific nutritional details for one item (e.g., Apple)."""
    return await services.get_commodity_by_name(session, name)