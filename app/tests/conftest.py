import asyncio
import json
from datetime import datetime

from httpx import AsyncClient
from pytest import fixture
from sqlalchemy import insert

from app.config import settings
from app.database.database import Base, engine
from app.dependencies.unit_of_work import get_unit_of_work
from app.main import app as fastapi_app
from app.models.bookings import Bookings
from app.models.hotels import Hotels
from app.models.rooms import Rooms
from app.models.users import Users


@fixture(scope="session", autouse=True)
async def reload_database():
    if settings.MODE == "TEST":
        async with engine.begin() as connection:
            await connection.run_sync(Base.metadata.drop_all)
            await connection.run_sync(Base.metadata.create_all)

        def open_file_json(model: str):
            with open(f"app/tests/data_tests/mock_{model}.json", encoding="utf-8") as file:
                return json.load(file)

        users = open_file_json("users")
        hotels = open_file_json("hotels")
        rooms = open_file_json("rooms")
        bookings = open_file_json("bookings")

        for booking in bookings:
            booking["date_from"] = datetime.strptime(booking["date_from"], "%Y-%m-%d")
            booking["date_to"] = datetime.strptime(booking["date_to"], "%Y-%m-%d")

        async with get_unit_of_work() as uow:
            for model, values in ((Hotels, hotels), (Rooms, rooms), (Users, users), (Bookings, bookings)):
                query = insert(model).values(values)
                await uow.session.execute(query)


@fixture(scope="function")
async def async_client():
    async with AsyncClient(app=fastapi_app, base_url="http://test") as async_client:
        yield async_client


@fixture(scope="function")
async def auth_async_client():
    async with AsyncClient(app=fastapi_app, base_url="http://test") as async_client:
        await async_client.post("/auth/login", json={"email": "user@example.com", "password": "Aa@12345"})
        assert async_client.cookies.get("booking_access_token")
        yield async_client


@fixture(scope="session")
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
