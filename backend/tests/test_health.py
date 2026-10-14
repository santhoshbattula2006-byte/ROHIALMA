import pytest
from fastapi import status


@pytest.mark.asyncio
async def test_health_check_endpoint(async_client):
    response = await async_client.get("/api/v1/health")
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data["status"] == "healthy"
    assert "app_name" in data
    assert "environment" in data
    assert "version" in data
