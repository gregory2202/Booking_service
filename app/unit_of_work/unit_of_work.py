from types import TracebackType
from typing import Self

from app.database.database import async_session_maker
from app.interfaces.unit_of_work import IUnitOfWork
from app.repositories.bookings import SQLAlchemyBookingsRepository
from app.repositories.hotels import SQLAlchemyHotelsRepository
from app.repositories.rooms import SQLAlchemyRoomsRepository
from app.repositories.users import SQLAlchemyUsersRepository


class SQLAlchemyUnitOfWork(IUnitOfWork):
    def __init__(self) -> None:
        self.session_factory = async_session_maker

    async def __aenter__(self) -> Self:
        self.session = self.session_factory()

        self.users_repository = SQLAlchemyUsersRepository(self.session)
        self.bookings_repository = SQLAlchemyBookingsRepository(self.session)
        self.hotels_repository = SQLAlchemyHotelsRepository(self.session)
        self.rooms_repository = SQLAlchemyRoomsRepository(self.session)

        return self

    async def __aexit__(self, exc_type: BaseException | None, exc_val: BaseException | None,
                        exc_tb: TracebackType | None) -> bool:
        if exc_type:
            await self.rollback()
        else:
            await self.session.commit()
        await self.session.close()
        return False

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()
