from app.database.database import async_session_maker
from app.interfaces.unit_of_work import IUnitOfWork
from app.repositories.bookings import SQLAlchemyBookingsRepository
from app.repositories.hotels import SQLAlchemyHotelsRepository
from app.repositories.rooms import SQLAlchemyRoomsRepository
from app.repositories.users import SQLAlchemyUsersRepository


class SQLAlchemyUnitOfWork(IUnitOfWork):
    def __init__(self):
        self.session_factory = async_session_maker

    async def __aenter__(self):
        self.session = self.session_factory()

        self.users_repository = SQLAlchemyUsersRepository(self.session)
        self.bookings_repository = SQLAlchemyBookingsRepository(self.session)
        self.hotels_repository = SQLAlchemyHotelsRepository(self.session)
        self.rooms_repository = SQLAlchemyRoomsRepository(self.session)

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            await self.rollback()
        else:
            await self.session.commit()
        await self.session.close()
        return False

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
