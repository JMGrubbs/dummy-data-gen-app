"""Health and dependency checks used by the health endpoints."""

from __future__ import annotations

import asyncio
from datetime import UTC, datetime

from cache.redis import redis_manager
from db.session import engine
from sqlalchemy import text


async def check_database() -> bool:
    try:
        async with engine.connect() as connection:
            await connection.execute(text("SELECT 1"))
        return True
    except Exception:
        return False


async def check_cache() -> bool:
    try:
        await redis_manager.get_client().ping()
        return True
    except Exception:
        return False


async def dependencies_ready() -> bool:
    database_ready, cache_ready = await asyncio.gather(check_database(), check_cache())
    return database_ready and cache_ready


def live_payload() -> dict[str, str]:
    return {"status": "alive", "timestamp": datetime.now(UTC).isoformat()}
