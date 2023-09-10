from fastapi import APIRouter, Depends

from app.dependencies.bookings import get_bookings_services
from app.dependencies.users import get_current_user
from app.services.bookings import BookingsServices
from app.models.users import Users
from app.schemas.bookings import SBookingInfo, SNewBooking

router = APIRouter(prefix="/bookinks", tags=["Бронирования"])


@router.get("")
async def get_bookings(bookings_services: BookingsServices = Depends(get_bookings_services),
                       user: Users = Depends(get_current_user)) -> list[SBookingInfo]:
    return await bookings_services.get_bookings(user)


@router.post("")
async def add_booking(new_booking: SNewBooking, bookings_services: BookingsServices = Depends(get_bookings_services),
                      user: Users = Depends(get_current_user)):
    booking = await bookings_services.add_booking(new_booking, user)
    await bookings_services.send_booking_confirmation_email(booking)
    return booking


@router.post("/{booking_id}")
async def remove_booking(booking_id: int, bookings_services: BookingsServices = Depends(get_bookings_services),
                         user: Users = Depends(get_current_user)) -> None:
    await bookings_services.remove_booking(booking_id, user)