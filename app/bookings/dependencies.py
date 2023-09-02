from app.bookings.repository import BookingRepository
from app.bookings.services import BookingsServices


def get_bookings_services():
    return BookingsServices(BookingRepository())
