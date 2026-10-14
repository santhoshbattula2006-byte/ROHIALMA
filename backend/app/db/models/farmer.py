from typing import TYPE_CHECKING, Optional

from sqlalchemy import Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.db.models.base import TimestampMixin

if TYPE_CHECKING:
    from app.db.models.crop import Crop
    from app.db.models.location import Location
    from app.db.models.recommendation import Recommendation
    from app.db.models.soil import SoilProfile
    from app.db.models.user import User


class FarmerProfile(Base, TimestampMixin):
    __tablename__ = "farmer_profiles"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )
    location_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("locations.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    primary_crop_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("crops.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    land_area_acres: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    preferred_language: Mapped[str] = mapped_column(
        String(10), default="en", nullable=False
    )

    user: Mapped["User"] = relationship("User", back_populates="farmer_profile")
    location: Mapped[Optional["Location"]] = relationship(
        "Location", back_populates="farmer_profiles"
    )
    primary_crop: Mapped[Optional["Crop"]] = relationship(
        "Crop", back_populates="farmer_profiles"
    )
    soil_profiles: Mapped[list["SoilProfile"]] = relationship(
        "SoilProfile", back_populates="farmer_profile", cascade="all, delete-orphan"
    )
    recommendations: Mapped[list["Recommendation"]] = relationship(
        "Recommendation", back_populates="farmer_profile", cascade="all, delete-orphan"
    )
