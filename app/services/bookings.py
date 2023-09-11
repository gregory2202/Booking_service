from app.exceptions.exceptions import RoomCannotBeBooked, ReservationNotFoundError
from app.models.users import Users
from app.repositories.bookings import BookingsRepository
from app.schemas.bookings import SNewBooking


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
        booking = await self.bookings_repository.find_one_or_none(id=booking_id, user_id=user.id)
        if not booking:
            raise ReservationNotFoundError
        await self.bookings_repository.delete(id=booking_id, user_id=user.id)
        return {"message": "Бронь успешно удалена", "reservation_id": booking_id}
