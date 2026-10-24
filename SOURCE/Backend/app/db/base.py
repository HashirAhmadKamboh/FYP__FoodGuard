from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs

class Base(AsyncAttrs, DeclarativeBase):
    pass


from app.modules.commodities import models as commodities_models
from app.modules.prices import models as prices_models
from app.account import models as account_models