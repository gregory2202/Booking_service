from datetime import date

from app.repositories.hotels import HotelsRepositoryAbstract


class HotelsServices:
    def __init__(self, hotels_repository: HotelsRepositoryAbstract):
        self.hotels_repository = hotels_repository

    async def get_hotels_by_location_and_time(self, location: str, date_from: date, date_to: date):
        return await self.hotels_repository.find_all(location=location, date_from=date_from, date_to=date_to)

    async def get_hotel_by_id(self, hotel_id: int):
        return await self.hotels_repository.find_one_or_none(id=hotel_id)
