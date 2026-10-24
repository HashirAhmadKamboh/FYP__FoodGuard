from fastapi import APIRouter
from typing import List
from app.db.session import SessionDep
from .schemas import PriceRecordOut
from . import services

router = APIRouter(prefix="/api/prices", tags=["Prices"])

@router.get("/{city}", response_model=List[PriceRecordOut])
async def get_city_prices(session: SessionDep, city: str):
    """Get all scraped prices for a specific district/city."""
    return await services.get_prices_by_city(session, city)