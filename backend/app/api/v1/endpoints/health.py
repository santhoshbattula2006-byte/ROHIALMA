from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import check_database_connection, get_db
from app.core.logging import logger

router = APIRouter()


class HealthResponse(BaseModel):
    status: str
    app_name: str
    environment: str
    version: str


class DatabaseHealthResponse(BaseModel):
    status: str
    database: str
    latency_ms: float | None = None
    detail: str | None = None


@router.get(
    "/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Application Health Check",
    description=(
        "Returns current application operational status and environment details."
    ),
)
async def get_health() -> HealthResponse:
    return HealthResponse(
        status="healthy",
        app_name=settings.APP_NAME,
        environment=settings.APP_ENV,
        version="0.1.0",
    )


@router.get(
    "/health/db",
    response_model=DatabaseHealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Database Connectivity Check",
    description="Performs a real execution query against the database.",
)
async def get_db_health(
    db: AsyncSession = Depends(get_db),
) -> DatabaseHealthResponse:
    try:
        health_info = await check_database_connection(db)
        return DatabaseHealthResponse(
            status=health_info["status"],
            database=health_info["database"],
            latency_ms=health_info["latency_ms"],
        )
    except Exception as exc:
        logger.error(f"Database health check failed: {exc}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=DatabaseHealthResponse(
                status="unhealthy",
                database="disconnected",
                detail=str(exc),
            ).model_dump(),
        )
