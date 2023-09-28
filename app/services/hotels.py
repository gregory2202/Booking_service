from datetime import date

from app.exceptions.exceptions import (
    ExcessiveBookingDurationError,
    HotelNotFoundError,
    InvalidDateError,
    LocationNotFoundError,
)
from app.interfaces.unit_of_work import IUnitOfWork


class HotelsServices:
    def __init__(self, unit_of_work: IUnitOfWork):
        self.unit_of_work = unit_of_work

    async def get_hotels_by_location_and_time(self, location: str, date_from: date, date_to: date):
        if date_from > date_to:
            raise InvalidDateError
        if (date_to - date_from).days > 30:
            raise ExcessiveBookingDurationError

        async with self.unit_of_work as uow:
            hotels = await uow.hotels_repository.find_all(location=location, date_from=date_from, date_to=date_to)

        if not hotels:
            raise LocationNotFoundError

        return hotels

    async def get_hotel_by_id(self, hotel_id: int):
        async with self.unit_of_work as uow:
            hotel = await uow.hotels_repository.find_one_or_none(id=hotel_id)

        if not hotel:
            raise HotelNotFoundError

        return hotel
