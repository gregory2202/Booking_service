from datetime import date

from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache

from app.hotels.rooms.dependencies import get_rooms_services
from app.hotels.rooms.services import RoomsServices
from app.hotels.rooms.schemas import SRoomInfo

router = APIRouter()


@router.get("/{hotel_id}/rooms")
@cache(expire=60)
async def get_rooms_by_date(hotel_id: int, date_from: date, date_to: date,
                            rooms_services: RoomsServices = Depends(get_rooms_services)) -> list[SRoomInfo]:
    return await rooms_services.get_rooms_by_date(hotel_id=hotel_id, date_from=date_from, date_to=date_to)
