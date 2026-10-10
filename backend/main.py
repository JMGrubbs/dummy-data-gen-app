from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings
from middleware.request_id import RequestIDMiddleware
from httpxC.http_client import http_client
from cache.redis import redis_manager
from api.v1.api import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await redis_manager.connect()
    yield
    await redis_manager.disconnect()
    await http_client.aclose()


app = FastAPI(
    title="Dummy Data Generator API",
    lifespan=lifespan,
)

app.add_middleware(RequestIDMiddleware)

app.add_middleware(
    CORSMiddleware,
    # Keep the configured frontend origin(s) explicit for credentialed cookies,
    # while allowing the known local/dev hosts used by the Compose deployment.
    allow_origins=[
        origin.strip().rstrip("/")
        for origin in (settings.frontend_origins or settings.frontend_url).split(",")
        if origin.strip()
    ],
    allow_origin_regex=r"^https?://(localhost|127\.0\.0\.1|vm-work-dev-db\.tail0c3733\.ts\.net)(:\d+)?$",
    allow_credentials=True,
    allow_methods=[
        "GET",
        "POST",
        "PUT",
        "PATCH",
        "DELETE",
        "OPTIONS",
    ],
    allow_headers=[
        "Accept",
        "Authorization",
        "Content-Type",
        "Origin",
    ],
)

app.include_router(api_router, prefix="/api/v1")
