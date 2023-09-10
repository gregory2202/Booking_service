from datetime import date

from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache

from app.controllers.rooms import router as router_books
from app.dependencies.hotels import get_hotels_services
from app.services.hotels import HotelsServices
from app.schemas.hotels import SHotel, SHotelInfo

router = APIRouter(prefix="/hotels", tags=["Отели"])
router.include_router(router_books)


@router.get("/{location}")
@cache(expire=60)
async def get_hotels_by_location_and_time(location: str, date_from: date, date_to: date,
                                          hotels_services: HotelsServices = Depends(get_hotels_services)) -> \
        list[SHotelInfo]:
    return await hotels_services.get_hotels_by_location_and_time(location=location, date_from=date_from,
                                                                 date_to=date_to)


@router.get("/id/{hotel_id}")
async def get_hotel_by_id(hotel_id: int, hotels_services=Depends(get_hotels_services)) -> SHotel | None:
    return await hotels_services.get_hotel_by_id(hotel_id=hotel_id)
