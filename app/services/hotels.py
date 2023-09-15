from datetime import date

from app.interfaces.unit_of_work import IUnitOfWork


class HotelsServices:
    def __init__(self, unit_of_work: IUnitOfWork):
        self.unit_of_work = unit_of_work

    async def get_hotels_by_location_and_time(self, location: str, date_from: date, date_to: date):
        async with self.unit_of_work as uow:
            return await uow.hotels_repository.find_all(location=location, date_from=date_from, date_to=date_to)

    async def get_hotel_by_id(self, hotel_id: int):
        async with self.unit_of_work as uow:
            return await uow.hotels_repository.find_one_or_none(id=hotel_id)
