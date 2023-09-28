from abc import ABC, abstractmethod

from app.interfaces.repository import (
    IBookingsRepository,
    IHotelsRepository,
    IRoomsRepository,
    IUsersRepository,
)


class IUnitOfWork(ABC):
    users_repository: IUsersRepository
    bookings_repository: IBookingsRepository
    hotels_repository: IHotelsRepository
    rooms_repository: IRoomsRepository

    @abstractmethod
    async def __aenter__(self) -> "IUnitOfWork":
        raise NotImplementedError

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        raise NotImplementedError

    @abstractmethod
    async def commit(self):
        raise NotImplementedError

    @abstractmethod
    async def rollback(self):
        raise NotImplementedError
