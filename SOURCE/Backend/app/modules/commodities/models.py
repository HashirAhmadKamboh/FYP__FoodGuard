from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Float, ForeignKey
from app.db.base import Base

class Commodity(Base):
    __tablename__ = "commodities"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), index=True, unique=True)
    category: Mapped[str] = mapped_column(String(50))
    
    nutrition: Mapped["NutritionalProfile"] = relationship(back_populates="commodity", uselist=False)

class NutritionalProfile(Base):
    __tablename__ = "nutritional_profiles"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    commodity_id: Mapped[int] = mapped_column(ForeignKey("commodities.id"))
    
    energy_kcal: Mapped[float] = mapped_column(Float, nullable=True)
    protein_g: Mapped[float] = mapped_column(Float, nullable=True)
    fat_g: Mapped[float] = mapped_column(Float, nullable=True)
    carbs_g: Mapped[float] = mapped_column(Float, nullable=True)
    fiber_g: Mapped[float] = mapped_column(Float, nullable=True)
    water_pct: Mapped[str] = mapped_column(String(50), nullable=True)
    vitamins_minerals: Mapped[str] = mapped_column(String(255), nullable=True)
    phytochemicals: Mapped[str] = mapped_column(String(255), nullable=True)
    serving_size: Mapped[str] = mapped_column(String(100), nullable=True)

    commodity: Mapped["Commodity"] = relationship(back_populates="nutrition")