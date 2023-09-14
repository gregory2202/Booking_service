from fastapi import Depends

from app.dependencies.unit_of_work import get_unit_of_work
from app.interfaces.unit_of_work import IUnitOfWork
from app.services.auth import AuthServices
from app.services.bookings import BookingsServices
from app.services.email import EmailServices
from app.services.hotels import HotelsServices
from app.services.rooms import RoomsServices
from app.services.users import UsersServices


def get_auth_services(unit_of_work: IUnitOfWork = Depends(get_unit_of_work)) -> AuthServices:
    return AuthServices(unit_of_work)


def get_bookings_services(unit_of_work: IUnitOfWork = Depends(get_unit_of_work)) -> BookingsServices:
    return BookingsServices(unit_of_work)


def get_email_services(unit_of_work: IUnitOfWork = Depends(get_unit_of_work)) -> EmailServices:
    return EmailServices(unit_of_work)


def get_hotels_services(unit_of_work: IUnitOfWork = Depends(get_unit_of_work)) -> HotelsServices:
    return HotelsServices(unit_of_work)


def get_rooms_services(unit_of_work: IUnitOfWork = Depends(get_unit_of_work)) -> RoomsServices:
    return RoomsServices(unit_of_work)


def get_users_services(unit_of_work: IUnitOfWork = Depends(get_unit_of_work)) -> UsersServices:
    return UsersServices(unit_of_work)
