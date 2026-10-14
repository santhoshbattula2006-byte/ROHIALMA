
from unittest.mock import patch

import pytest
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.database import get_db
from app.main import app

# In-memory SQLite async engine for unit testing database connectivity
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture
async def test_db_session():
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
    await engine.dispose()


@pytest.mark.asyncio
async def test_db_health_success(async_client, test_db_session):
    async def override_get_db():
        yield test_db_session

    app.dependency_overrides[get_db] = override_get_db
    try:
        response = await async_client.get("/api/v1/health/db")
        assert response.status_code == status.HTTP_200_OK

        data = response.json()
        assert data["status"] == "healthy"
        assert data["database"] == "connected"
        assert "latency_ms" in data
        assert isinstance(data["latency_ms"], float)
    finally:
        app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_db_health_failure_behavior(async_client):
    with patch(
        "app.api.v1.endpoints.health.check_database_connection",
        side_effect=ConnectionError("Could not connect to PostgreSQL"),
    ):
        response = await async_client.get("/api/v1/health/db")
        assert response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE

        data = response.json()
        assert "detail" in data
        assert data["detail"]["status"] == "unhealthy"
        assert data["detail"]["database"] == "disconnected"


@pytest.mark.asyncio
async def test_unreachable_postgres_real_connection_failure(async_client):
    # Tests real un-mocked behavior when PostgreSQL host is not running
    response = await async_client.get("/api/v1/health/db")
    # Because PostgreSQL service is not running locally, it MUST fail with HTTP 503
    assert response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
    data = response.json()
    assert data["detail"]["status"] == "unhealthy"
    assert data["detail"]["database"] == "disconnected"
