from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import desc
from .models import PriceRecord

async def get_prices_by_city(session: AsyncSession, city_name: str):
    result = await session.execute(
        select(PriceRecord)
        .where(PriceRecord.city_name == city_name.lower())
        .order_by(desc(PriceRecord.scrape_date))
    )
    return result.scalars().all()