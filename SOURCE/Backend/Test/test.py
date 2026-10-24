import asyncio
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import AsyncSessionLocal
from app.modules.commodities.services import get_all_commodities

async def main():
    async with AsyncSessionLocal() as session:
        try:
            print("Fetching...")
            items = await get_all_commodities(session)
            print(f"Got {len(items)} items")
            from app.modules.commodities.schemas import CommodityOut
            for item in items:
                CommodityOut.model_validate(item)
            print("Validation successful")
        except Exception as e:
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
