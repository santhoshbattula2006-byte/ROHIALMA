from datetime import date, datetime
from typing import TYPE_CHECKING, Any, Optional

from sqlalchemy import JSON, Date, DateTime, Float, ForeignKey, Index, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.db.models.base import TimestampMixin

if TYPE_CHECKING:
    from app.db.models.location import Location


class WeatherCache(Base, TimestampMixin):
    __tablename__ = "weather_cache"
    __table_args__ = (
        Index("ix_weather_coords_date", "latitude", "longitude", "forecast_date"),
    )

    location_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("locations.id", ondelete="SET NULL"), nullable=True, index=True
    )
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    forecast_date: Mapped[date] = mapped_column(Date, index=True, nullable=False)

    temperature_min: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    temperature_max: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    humidity: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    rainfall_mm: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    wind_speed_kmh: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    weather_condition: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    # Genuine snapshot structure for raw weather provider JSON payload
    raw_response_json: Mapped[Optional[dict[str, Any]]] = mapped_column(
        JSON, nullable=True
    )
    fetched_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )

    location: Mapped[Optional["Location"]] = relationship(
        "Location", back_populates="weather_caches"
    )
