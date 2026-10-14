from typing import TYPE_CHECKING, Optional

from sqlalchemy import Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.db.models.base import TimestampMixin

if TYPE_CHECKING:
    from app.db.models.farmer import FarmerProfile
    from app.db.models.recommendation import Recommendation


class Crop(Base, TimestampMixin):
    __tablename__ = "crops"

    name: Mapped[str] = mapped_column(
        String(100), unique=True, index=True, nullable=False
    )
    scientific_name: Mapped[Optional[str]] = mapped_column(
        String(150), nullable=True
    )
    category: Mapped[Optional[str]] = mapped_column(
        String(50), nullable=True
    )  # Cereal, Pulse, etc.
    season: Mapped[Optional[str]] = mapped_column(
        String(50), nullable=True
    )  # Kharif, Rabi, Zaid
    min_duration_days: Mapped[Optional[int]] = mapped_column(
        Integer, nullable=True
    )
    max_duration_days: Mapped[Optional[int]] = mapped_column(
        Integer, nullable=True
    )

    farmer_profiles: Mapped[list["FarmerProfile"]] = relationship(
        "FarmerProfile", back_populates="primary_crop"
    )
    rules: Mapped[list["CropRule"]] = relationship(
        "CropRule", back_populates="crop", cascade="all, delete-orphan"
    )
    recommendations: Mapped[list["Recommendation"]] = relationship(
        "Recommendation", back_populates="crop"
    )


class CropRule(Base, TimestampMixin):
    __tablename__ = "crop_rules"

    crop_id: Mapped[int] = mapped_column(
        ForeignKey("crops.id", ondelete="CASCADE"), nullable=False, index=True
    )
    rule_name: Mapped[str] = mapped_column(String(100), nullable=False)
    min_ph: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    max_ph: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    min_n: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    max_n: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    min_p: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    max_p: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    min_k: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    max_k: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    min_rainfall_mm: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    max_rainfall_mm: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    priority: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

    crop: Mapped["Crop"] = relationship("Crop", back_populates="rules")
