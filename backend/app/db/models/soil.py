from datetime import date
from enum import Enum as PyEnum
from typing import TYPE_CHECKING, Optional

from sqlalchemy import (
    Date,
    Enum,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.db.models.base import TimestampMixin

if TYPE_CHECKING:
    from app.db.models.farmer import FarmerProfile
    from app.db.models.location import Location


class SoilSource(str, PyEnum):
    FARMER = "FARMER"
    BLOCK_DEFAULT = "BLOCK_DEFAULT"
    LAB_TEST = "LAB_TEST"
    ESTIMATED = "ESTIMATED"


class SoilProfile(Base, TimestampMixin):
    """Soil Profile with field-level provenance.

    Each soil parameter maintains its own explicit value and source provenance enum.
    """

    __tablename__ = "soil_profiles"

    farmer_profile_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("farmer_profiles.id", ondelete="CASCADE"), nullable=True, index=True
    )
    location_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("locations.id", ondelete="SET NULL"), nullable=True, index=True
    )
    sample_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    # Nitrogen (N)
    n_value: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    n_source: Mapped[Optional[SoilSource]] = mapped_column(
        Enum(SoilSource, native_enum=False), nullable=True
    )

    # Phosphorus (P)
    p_value: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    p_source: Mapped[Optional[SoilSource]] = mapped_column(
        Enum(SoilSource, native_enum=False), nullable=True
    )

    # Potassium (K)
    k_value: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    k_source: Mapped[Optional[SoilSource]] = mapped_column(
        Enum(SoilSource, native_enum=False), nullable=True
    )

    # pH Level
    ph_value: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    ph_source: Mapped[Optional[SoilSource]] = mapped_column(
        Enum(SoilSource, native_enum=False), nullable=True
    )

    # Organic Carbon (OC)
    oc_value: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    oc_source: Mapped[Optional[SoilSource]] = mapped_column(
        Enum(SoilSource, native_enum=False), nullable=True
    )

    # Electrical Conductivity (EC)
    ec_value: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    ec_source: Mapped[Optional[SoilSource]] = mapped_column(
        Enum(SoilSource, native_enum=False), nullable=True
    )

    # Micronutrients (Fe, Zn, B, S)
    fe_value: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    fe_source: Mapped[Optional[SoilSource]] = mapped_column(
        Enum(SoilSource, native_enum=False), nullable=True
    )
    zn_value: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    zn_source: Mapped[Optional[SoilSource]] = mapped_column(
        Enum(SoilSource, native_enum=False), nullable=True
    )
    b_value: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    b_source: Mapped[Optional[SoilSource]] = mapped_column(
        Enum(SoilSource, native_enum=False), nullable=True
    )
    s_value: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    s_source: Mapped[Optional[SoilSource]] = mapped_column(
        Enum(SoilSource, native_enum=False), nullable=True
    )

    farmer_profile: Mapped[Optional["FarmerProfile"]] = relationship(
        "FarmerProfile", back_populates="soil_profiles"
    )
    location: Mapped[Optional["Location"]] = relationship(
        "Location", back_populates="soil_profiles"
    )


class SoilDefaultDatasetRecord(Base, TimestampMixin):
    """Block-level Soil Default Dataset Record.

    Retains summary category data, raw sample counts, cycle, scheme source,
    state, district, and block information.
    """

    __tablename__ = "soil_default_dataset_records"
    __table_args__ = (
        UniqueConstraint(
            "state", "district", "block", "cycle", name="uq_soil_block_cycle"
        ),
        Index("ix_soil_default_location", "state", "district", "block"),
    )

    state: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    district: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    block: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    cycle: Mapped[str] = mapped_column(
        String(50), index=True, nullable=False
    )  # e.g., '2019-2022'
    scheme_source: Mapped[str] = mapped_column(
        String(150), default="Soil Health Card Scheme", nullable=False
    )

    # Derived Categories (Low / Medium / High / Acidic / Neutral / Alkaline)
    n_category: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    p_category: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    k_category: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    oc_category: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    ph_category: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    ec_category: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)

    # Raw Sample Counts
    n_count_low: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    n_count_medium: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    n_count_high: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    p_count_low: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    p_count_medium: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    p_count_high: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    k_count_low: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    k_count_medium: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    k_count_high: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    oc_count_low: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    oc_count_medium: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    oc_count_high: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    ph_count_acidic: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    ph_count_neutral: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    ph_count_alkaline: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    total_samples_tested: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
