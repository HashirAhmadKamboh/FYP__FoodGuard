from pydantic import BaseModel, ConfigDict
from typing import Optional

class PriceRecordOut(BaseModel):
    id: int
    city_name: str
    scrape_date: str
    category: str
    item_name: str
    min_price: Optional[float]
    max_price: Optional[float]
    fqp: Optional[float]
    dc_price: Optional[float]
    psba_price: Optional[float]
    source: Optional[str]

    model_config = ConfigDict(from_attributes=True)