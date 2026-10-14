import pytest
from sqlalchemy import inspect
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.database import Base
from app.db.models import (
    FarmerProfile,
    Location,
    SoilDefaultDatasetRecord,
    SoilProfile,
    SoilSource,
    User,
    UserRole,
)

TEST_DB_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture
async def async_test_session():
    engine = create_async_engine(TEST_DB_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session, engine

    await engine.dispose()


@pytest.mark.asyncio
async def test_all_tables_created(async_test_session):
    _, engine = async_test_session
    async with engine.connect() as conn:
        tables = await conn.run_sync(
            lambda sync_conn: inspect(sync_conn).get_table_names()
        )
    expected_tables = {
        "users",
        "farmer_profiles",
        "locations",
        "soil_profiles",
        "soil_default_dataset_records",
        "weather_cache",
        "crops",
        "crop_rules",
        "recommendations",
        "chat_sessions",
        "chat_messages",
    }
    assert expected_tables.issubset(set(tables))


@pytest.mark.asyncio
async def test_soil_profile_field_level_provenance(async_test_session):
    session, _ = async_test_session

    user = User(
        full_name="Ramesh Patel",
        phone_number="+919876543210",
        role=UserRole.FARMER,
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)

    farmer = FarmerProfile(user_id=user.id, land_area_acres=5.5)
    session.add(farmer)
    await session.commit()
    await session.refresh(farmer)

    soil = SoilProfile(
        farmer_profile_id=farmer.id,
        n_value=240.5,
        n_source=SoilSource.FARMER,
        p_value=45.0,
        p_source=SoilSource.FARMER,
        k_value=130.0,
        k_source=SoilSource.BLOCK_DEFAULT,
        ph_value=6.8,
        ph_source=SoilSource.LAB_TEST,
        oc_value=0.55,
        oc_source=SoilSource.BLOCK_DEFAULT,
    )
    session.add(soil)
    await session.commit()
    await session.refresh(soil)

    assert soil.n_value == 240.5
    assert soil.n_source == SoilSource.FARMER
    assert soil.k_value == 130.0
    assert soil.k_source == SoilSource.BLOCK_DEFAULT
    assert soil.ph_source == SoilSource.LAB_TEST


@pytest.mark.asyncio
async def test_location_hierarchy_without_village(async_test_session):
    session, _ = async_test_session

    loc1 = Location(
        state="Telangana",
        district="Warangal",
        block="Ghanpur",
        village=None,
    )
    session.add(loc1)
    await session.commit()
    await session.refresh(loc1)

    assert loc1.state == "Telangana"
    assert loc1.block == "Ghanpur"
    assert loc1.village is None


@pytest.mark.asyncio
async def test_soil_default_dataset_record(async_test_session):
    session, _ = async_test_session

    record = SoilDefaultDatasetRecord(
        state="Telangana",
        district="Warangal",
        block="Ghanpur",
        cycle="2019-2022",
        scheme_source="Soil Health Card Scheme",
        n_category="Medium",
        n_count_low=120,
        n_count_medium=450,
        n_count_high=80,
        total_samples_tested=650,
    )
    session.add(record)
    await session.commit()
    await session.refresh(record)

    assert record.block == "Ghanpur"
    assert record.n_count_medium == 450
    assert record.total_samples_tested == 650
