from app.models.bookings import Bookings
from app.repositories.bookings import BookingsRepository
from app.tasks.tasks import send_email


class EmailServices:
    def __init__(self, booking_repository: BookingsRepository):
        self.bookings_repository = booking_repository

    async def send_booking_confirmation_email(self, booking: Bookings):
        booking_data = await self.bookings_repository.find_data_for_mail(booking)
        send_email.delay(**booking_data)
