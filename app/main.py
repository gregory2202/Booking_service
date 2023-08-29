from fastapi import FastAPI

from app.bookings.router import router as router_bookings
from app.users.router import router_auth
from app.users.router import router_users
from app.hotels.router import router as router_hotels

app = FastAPI()

# Подключение основных роутеров
app.include_router(router_auth)
app.include_router(router_users)
app.include_router(router_hotels)
app.include_router(router_bookings)
