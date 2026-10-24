from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Float, Date
from app.db.base import Base

class PriceRecord(Base):
    __tablename__ = "price_records"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    city_name: Mapped[str] = mapped_column(String(50), index=True)
    scrape_date: Mapped[str] = mapped_column(String(20), index=True)
    category: Mapped[str] = mapped_column(String(100))
    item_id: Mapped[int] = mapped_column(nullable=True)
    item_name: Mapped[str] = mapped_column(String(100), index=True)
    min_price: Mapped[float] = mapped_column(Float, nullable=True)
    max_price: Mapped[float] = mapped_column(Float, nullable=True)
    fqp: Mapped[float] = mapped_column(Float, nullable=True)
    dc_price: Mapped[float] = mapped_column(Float, nullable=True)
    psba_price: Mapped[float] = mapped_column(Float, nullable=True)
    source: Mapped[str] = mapped_column(String(50), nullable=True, default="Unknown")