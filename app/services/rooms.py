from datetime import date

from app.interfaces.unit_of_work import IUnitOfWork


class RoomsServices:
    def __init__(self, unit_of_work: IUnitOfWork):
        self.unit_of_work = unit_of_work

    async def get_rooms_by_date(self, hotel_id: int, date_from: date, date_to: date):
        async with self.unit_of_work as session:
            return await session.rooms_repository.find_all(hotel_id=hotel_id, date_from=date_from, date_to=date_to)
