from datetime import date

from fastapi import APIRouter
from fastapi_cache.decorator import cache

from app.hotels.dao import HotelDao
from app.hotels.schemas import SHotel, SHotelInfo
from app.hotels.rooms.router import router as router_books

router = APIRouter(prefix="/hotels", tags=["Отели"])
router.include_router(router_books)


@router.get("/{location}")
@cache(expire=60)
async def get_hotels_by_location_and_time(location: str, date_from: date, date_to: date) -> list[SHotelInfo]:
    return await HotelDao.find_all(location=location, date_from=date_from, date_to=date_to)


@router.get("/id/{hotel_id}")
async def get_hotel_by_id(hotel_id: int) -> SHotel | None:
    return await HotelDao.find_one_or_none(id=hotel_id)
