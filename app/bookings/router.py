from datetime import date

from fastapi import APIRouter, Depends

from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBookingInfo
from app.users.models import Users
from app.users.dependencies import get_current_user
from app.exceptions import RoomCannotBeBooked

router = APIRouter(prefix="/bookinks", tags=["Бронирования"])


@router.get("")
async def get_bookings(user: Users = Depends(get_current_user)) -> list[SBookingInfo]:
    return await BookingDAO.find_all_with_images(user_id=user.id)


@router.post("")
async def add_booking(room_id: int, date_from: date, date_to: date, user: Users = Depends(get_current_user)):
    booking = await BookingDAO.add(user.id, room_id, date_from, date_to)
    if not booking:
        raise RoomCannotBeBooked
    return booking


@router.post("/{booking_id}")
async def remove_booking(booking_id: int, user: Users = Depends(get_current_user)) -> None:
    await BookingDAO.delete(id=booking_id, user_id=user.id)
