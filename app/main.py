from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from app.bookings.router import router as router_bookings
from app.users.router import router_auth
from app.users.router import router_users
from app.hotels.router import router as router_hotels
from app.config import settings


# Настройка lifespan приложения
@asynccontextmanager
async def lifespan(application: FastAPI):
    redis = aioredis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}", encoding="utf8",
                              decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="cache")
    yield


app = FastAPI(lifespan=lifespan)

# Подключение основных роутеров
app.include_router(router_auth)
app.include_router(router_users)
app.include_router(router_hotels)
app.include_router(router_bookings)
