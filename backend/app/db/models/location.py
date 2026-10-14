from typing import TYPE_CHECKING, Optional

from sqlalchemy import Float, Index, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.db.models.base import TimestampMixin

if TYPE_CHECKING:
    from app.db.models.farmer import FarmerProfile
    from app.db.models.soil import SoilProfile
    from app.db.models.weather import WeatherCache


class Location(Base, TimestampMixin):
    __tablename__ = "locations"
    __table_args__ = (
        UniqueConstraint(
            "state", "district", "block", "village", name="uq_location_hierarchy"
        ),
        Index("ix_location_hierarchy", "state", "district", "block"),
    )

    state: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    district: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    block: Mapped[str] = mapped_column(
        String(100), index=True, nullable=False
    )  # Block / Mandal
    village: Mapped[Optional[str]] = mapped_column(
        String(100), index=True, nullable=True
    )  # Explicit optional village level
    pincode: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    latitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    longitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    farmer_profiles: Mapped[list["FarmerProfile"]] = relationship(
        "FarmerProfile", back_populates="location"
    )
    soil_profiles: Mapped[list["SoilProfile"]] = relationship(
        "SoilProfile", back_populates="location"
    )
    weather_caches: Mapped[list["WeatherCache"]] = relationship(
        "WeatherCache", back_populates="location"
    )
