from datetime import date

from app.exceptions.exceptions import HotelNotFoundError, InvalidDateError, ExcessiveBookingDurationError
from app.interfaces.unit_of_work import IUnitOfWork


class RoomsServices:
    def __init__(self, unit_of_work: IUnitOfWork):
        self.unit_of_work = unit_of_work

    async def get_rooms_by_date(self, hotel_id: int, date_from: date, date_to: date):
        if date_from > date_to:
            raise InvalidDateError
        if (date_to - date_from).days > 30:
            raise ExcessiveBookingDurationError

        async with self.unit_of_work as uow:
            if not await uow.hotels_repository.find_one_or_none(id=hotel_id):
                raise HotelNotFoundError
            return await uow.rooms_repository.find_all(hotel_id=hotel_id, date_from=date_from, date_to=date_to)
