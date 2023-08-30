from datetime import date

from fastapi import APIRouter
from fastapi_cache.decorator import cache

from app.hotels.rooms.dao import RoomsDAO
from app.hotels.rooms.schemas import SRoomInfo

router = APIRouter()


@router.get("/{hotel_id}/rooms")
@cache(expire=60)
async def get_rooms_by_date(hotel_id: int, date_from: date, date_to: date) -> list[SRoomInfo]:
    return await RoomsDAO.find_all(hotel_id=hotel_id, date_from=date_from, date_to=date_to)
