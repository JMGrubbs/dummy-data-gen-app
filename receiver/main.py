from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from api.v1.api import api_router
from cache.redis import redis_manager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from httpxC.http_client import http_client


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    await redis_manager.connect()
    yield
    await redis_manager.disconnect()
    await http_client.aclose()


app = FastAPI(
    title="Data Receiver API",
    lifespan=lifespan,
)


app.add_middleware(
    middleware_class=CORSMiddleware,
    # Keep the configured frontend origin(s) explicit for credentialed cookies,
    # while allowing the known local/dev hosts used by the Compose deployment.
    allow_credentials=True,
    allow_methods=[
        "GET",
        "POST",
        "PUT",
        "PATCH",
        "DELETE",
        "OPTIONS",
    ],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")
