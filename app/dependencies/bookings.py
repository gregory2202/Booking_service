from app.repositories.bookings import BookingsRepository
from app.services.bookings import BookingsServices


def get_bookings_services():
    return BookingsServices(BookingsRepository)
