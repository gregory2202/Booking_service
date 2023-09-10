from fastapi import Depends

from app.dependencies.unit_of_work import get_unit_of_work
from app.interfaces.unit_of_work import SQLAlchemyUnitOfWork
from app.repositories.bookings import BookingsRepository
from app.repositories.hotels import HotelsRepository
from app.repositories.rooms import RoomsRepository
from app.repositories.users import UsersRepository


def get_users_repository(unit_of_work: SQLAlchemyUnitOfWork = Depends(get_unit_of_work)):
    return UsersRepository(session=unit_of_work.session)


def get_bookings_repository(unit_of_work: SQLAlchemyUnitOfWork = Depends(get_unit_of_work)):
    return BookingsRepository(session=unit_of_work.session)


def get_hotels_repository(unit_of_work: SQLAlchemyUnitOfWork = Depends(get_unit_of_work)):
    return HotelsRepository(session=unit_of_work.session)


def get_rooms_repository(unit_of_work: SQLAlchemyUnitOfWork = Depends(get_unit_of_work)):
    return RoomsRepository(session=unit_of_work.session)
