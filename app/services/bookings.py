from app.exceptions.exceptions import RoomCannotBeBooked
from app.models.bookings import Bookings
from app.models.users import Users
from app.repositories.bookings import BookingsRepository
from app.schemas.bookings import SNewBooking
from app.tasks.tasks import send_email


class BookingsServices:
    def __init__(self, booking_repository: BookingsRepository):
        self.bookings_repository = booking_repository

    async def get_bookings(self, user: Users):
        return await self.bookings_repository.find_all_with_images(user_id=user.id)

    async def add_booking(self, booking: SNewBooking, user: Users):
        booking = await self.bookings_repository.add(user.id, booking.room_id, booking.date_from, booking.date_to)
        if not booking:
            raise RoomCannotBeBooked
        return booking

    async def remove_booking(self, booking_id: int, user: Users):
        await self.bookings_repository.delete(id=booking_id, user_id=user.id)
        #  Написать ответ пользователю, работа с исключениями

    async def send_booking_confirmation_email(self, booking: Bookings):
        booking_data = await self.bookings_repository.find_data_for_mail(booking)
        send_email.delay(**booking_data)
