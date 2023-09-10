from datetime import date

from app.repositories.rooms import RoomsRepository


class RoomsServices:
    def __init__(self, rooms_repository: RoomsRepository):
        self.rooms_repository = rooms_repository

    async def get_rooms_by_date(self, hotel_id: int, date_from: date, date_to: date):
        return await self.rooms_repository.find_all(hotel_id=hotel_id, date_from=date_from, date_to=date_to)
