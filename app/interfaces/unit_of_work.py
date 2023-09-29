from abc import ABC, abstractmethod
from types import TracebackType

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
    async def __aexit__(self, exc_type: BaseException | None, exc_val: BaseException | None,
                        exc_tb: TracebackType | None) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def commit(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def rollback(self) -> None:
        raise NotImplementedError
