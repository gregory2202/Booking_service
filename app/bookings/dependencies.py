from app.bookings.repository import BookingsRepository
from app.bookings.services import BookingsServices


def get_bookings_services():
    return BookingsServices(BookingsRepository())
