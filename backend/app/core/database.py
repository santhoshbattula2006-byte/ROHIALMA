import time
from typing import AsyncGenerator

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings
from app.core.logging import logger


class Base(DeclarativeBase):
    """Base declarative class for SQLAlchemy ORM models."""

    pass


# Database Engine Initialization
engine = create_async_engine(
    settings.async_database_url,
    echo=settings.DEBUG,
    future=True,
    pool_pre_ping=True,
)

# Async Session Factory
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency providing a transactional database session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception as exc:
            await session.rollback()
            logger.error(f"Database session rollback due to error: {exc}")
            raise
        finally:
            await session.close()


async def check_database_connection(session: AsyncSession | None = None) -> dict:
    """Performs a real database connectivity check by executing a query.

    Returns health metrics dictionary or raises an exception if unreachable.
    """
    start_time = time.perf_counter()
    if session is not None:
        result = await session.execute(text("SELECT 1"))
        _ = result.scalar()
    else:
        async with AsyncSessionLocal() as standalone_session:
            result = await standalone_session.execute(text("SELECT 1"))
            _ = result.scalar()
    latency_ms = round((time.perf_counter() - start_time) * 1000, 2)
    return {
        "status": "healthy",
        "database": "connected",
        "latency_ms": latency_ms,
    }
