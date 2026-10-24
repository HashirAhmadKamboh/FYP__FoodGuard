from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from fastapi import HTTPException
from .models import Commodity

async def get_all_commodities(session: AsyncSession):
    result = await session.execute(
        select(Commodity).options(selectinload(Commodity.nutrition))
    )
    return result.scalars().all()

async def get_commodity_by_name(session: AsyncSession, name: str):
    result = await session.execute(
        select(Commodity)
        .options(selectinload(Commodity.nutrition))
        .where(Commodity.name.ilike(f"%{name}%"))
    )
    commodity = result.scalars().first()
    if not commodity:
        raise HTTPException(status_code=404, detail="Commodity not found")
    return commodity