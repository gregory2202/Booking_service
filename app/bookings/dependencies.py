from app.bookings.repository import BookingRepository
from app.bookings.services import BookingsServices


def booking_services():
    return BookingsServices(BookingRepository())
