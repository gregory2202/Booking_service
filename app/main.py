from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from sqladmin import Admin

from app.admin.auth import authentication_backend
from app.admin.views import UsersAdmin, BookingsAdmin, HotelsAdmin, RoomsAdmin
from app.config import settings
from app.controllers.auth import router as router_auth
from app.controllers.bookings import router as router_bookings
from app.controllers.hotels import router as router_hotels
from app.controllers.users import router as router_users
from app.database.database import engine


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

#  Создание и подключение административной панели
admin = Admin(app, engine, authentication_backend=authentication_backend)

admin.add_view(UsersAdmin)
admin.add_view(BookingsAdmin)
admin.add_view(HotelsAdmin)
admin.add_view(RoomsAdmin)
