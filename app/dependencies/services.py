from fastapi import Depends

from app.dependencies.repositories import (
    get_users_repository, get_bookings_repository, get_hotels_repository, get_rooms_repository
)
from app.repositories.bookings import BookingsRepository
from app.repositories.hotels import HotelsRepository
from app.repositories.rooms import RoomsRepository
from app.repositories.users import UsersRepository
from app.services.auth import AuthServices
from app.services.bookings import BookingsServices
from app.services.email import EmailServices
from app.services.hotels import HotelsServices
from app.services.rooms import RoomsServices
from app.services.users import UsersServices


def get_auth_services(repository: UsersRepository = Depends(get_users_repository)):
    return AuthServices(repository)


def get_users_services(repository: UsersRepository = Depends(get_users_repository)):
    return UsersServices(repository)


def get_bookings_services(repository: BookingsRepository = Depends(get_bookings_repository)):
    return BookingsServices(repository)


def get_hotels_services(repository: HotelsRepository = Depends(get_hotels_repository)):
    return HotelsServices(repository)


def get_rooms_services(repository: RoomsRepository = Depends(get_rooms_repository)):
    return RoomsServices(repository)


def get_email_services(repository: RoomsRepository = Depends(get_bookings_repository)):
    return EmailServices(repository)
