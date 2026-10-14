from typing import TYPE_CHECKING, Any, Optional

from sqlalchemy import JSON, Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.db.models.base import TimestampMixin

if TYPE_CHECKING:
    from app.db.models.crop import Crop
    from app.db.models.farmer import FarmerProfile


class Recommendation(Base, TimestampMixin):
    __tablename__ = "recommendations"

    farmer_profile_id: Mapped[int] = mapped_column(
        ForeignKey("farmer_profiles.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    crop_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("crops.id", ondelete="SET NULL"), nullable=True, index=True
    )
    recommendation_type: Mapped[str] = mapped_column(
        String(50), nullable=False, index=True
    )  # e.g., CROP_SELECTION, FERTILIZER, IRRIGATION
    confidence_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)

    # Genuine snapshot structure capturing farmer soil, location & weather
    input_snapshot_json: Mapped[Optional[dict[str, Any]]] = mapped_column(
        JSON, nullable=True
    )
    # Genuine structured output (dosages, schedule, step-by-step instructions)
    details_json: Mapped[Optional[dict[str, Any]]] = mapped_column(
        JSON, nullable=True
    )

    farmer_profile: Mapped["FarmerProfile"] = relationship(
        "FarmerProfile", back_populates="recommendations"
    )
    crop: Mapped[Optional["Crop"]] = relationship(
        "Crop", back_populates="recommendations"
    )
