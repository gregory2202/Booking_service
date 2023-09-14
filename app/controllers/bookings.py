from fastapi import APIRouter, Depends

from app.dependencies.auth import get_current_user
from app.dependencies.services import get_bookings_services, get_email_services
from app.models.users import Users
from app.schemas.bookings import SBookingInfo, SNewBooking, SBooking, SDeleteBooking
from app.services.bookings import BookingsServices
from app.services.email import EmailServices

router = APIRouter(prefix="/bookinks", tags=["Бронирования"])


@router.get("")
async def get_bookings(bookings_services: BookingsServices = Depends(get_bookings_services),
                       user: Users = Depends(get_current_user)) -> list[SBookingInfo]:
    return await bookings_services.get_bookings(user)


@router.post("")
async def add_booking(new_booking: SNewBooking, bookings_services: BookingsServices = Depends(get_bookings_services),
                      email_services: EmailServices = Depends(get_email_services),
                      user: Users = Depends(get_current_user)) -> SBooking:
    booking = await bookings_services.add_booking(new_booking, user)
    await email_services.send_booking_confirmation_email(booking.id)
    return booking


@router.post("/{booking_id}")
async def remove_booking(booking_id: int, bookings_services: BookingsServices = Depends(get_bookings_services),
                         user: Users = Depends(get_current_user)) -> SDeleteBooking:
    return await bookings_services.remove_booking(booking_id, user)
