from contextlib import asynccontextmanager
import sentry_sdk
import time
from typing import AsyncIterator
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi_versioning import VersionedFastAPI

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from sqladmin import Admin

from app.config import settings
from app.database import engine
from app.logger import logger
from app.admin.views import BookingsAdmin, HotelsAdmin, RoomsAdmin, UsersAdmin

from app.admin.auth import authentication_backend
from app.bookings.router import router as router_bookings
from app.users.router import router as router_users
from app.hotels.router import router as router_hotels
from app.hotels.rooms.router import router as router_rooms

from app.pages.router import router as router_pages
from app.images.router import router as router_images

@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="cache")
    yield

sentry_sdk.init(
    dsn=settings.DSN,
    send_default_pii=True,
    traces_sample_rate=1.0,
    _experiments={
        "continuous_profiling_auto_start": True,
    },
)

app = FastAPI(lifespan=lifespan)

app.include_router(router_users)
app.include_router(router_bookings)
app.include_router(router_hotels)
app.include_router(router_rooms)

app.include_router(router_pages)
app.include_router(router_images)

origins= [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers",
                   "Access-Control-Allow-Origin",
                   "Authorization"],
)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    logger.info("Request execution time", extra={
        "process_time": round(process_time, 4)
    })
    return response

app = VersionedFastAPI(app,
    version_format='{major}',
    prefix_format='/v{major}',
    # description='Greet users with a nice message',
    # middleware=[
    #     Middleware(SessionMiddleware, secret_key='mysecretkey')
    # ]
)

admin = Admin(app, engine, authentication_backend=authentication_backend)

admin.add_view(UsersAdmin)
admin.add_view(BookingsAdmin)
admin.add_view(RoomsAdmin)
admin.add_view(HotelsAdmin)

app.mount("/static", StaticFiles(directory="app/static"), name="static")