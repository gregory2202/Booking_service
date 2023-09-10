from app.database.database import async_session_maker
from app.interfaces.unit_of_work import SQLAlchemyUnitOfWork


async def get_unit_of_work():
    async with SQLAlchemyUnitOfWork(async_session_maker) as unit_of_work:
        yield unit_of_work
