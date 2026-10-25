"""Health and dependency checks used by the health endpoints."""

from __future__ import annotations

import asyncio
from datetime import UTC, datetime

from cache.redis import redis_manager


async def check_cache() -> bool:
    try:
        redis_manager.get_client().ping()
        return True
    except Exception:
        return False


async def dependencies_ready() -> tuple[bool]:
    cache_ready: tuple[bool] = await asyncio.gather(check_cache())
    return cache_ready


def live_payload() -> dict[str, str]:
    return {"status": "alive", "timestamp": datetime.now(UTC).isoformat()}
