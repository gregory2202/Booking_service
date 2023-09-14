from app.exceptions.exceptions import RoomCannotBeBooked, ReservationNotFoundError
from app.interfaces.unit_of_work import IUnitOfWork
from app.models.users import Users
from app.schemas.bookings import SNewBooking


class BookingsServices:
    def __init__(self, unit_of_work: IUnitOfWork):
        self.unit_of_work = unit_of_work

    async def get_bookings(self, user: Users):
        async with self.unit_of_work as session:
            return await session.bookings_repository.find_all_with_images(user_id=user.id)

    async def add_booking(self, booking: SNewBooking, user: Users):
        async with self.unit_of_work as session:
            booking = await session.bookings_repository.add(user_id=user.id, room_id=booking.room_id,
                                                            date_from=booking.date_from,
                                                            date_to=booking.date_to)
            if not booking:
                raise RoomCannotBeBooked
            return booking

    async def remove_booking(self, booking_id: int, user: Users):
        async with self.unit_of_work as session:
            booking = session.bookings_repository.find_one_or_none(id=booking_id, user_id=user.id)
            if not booking:
                raise ReservationNotFoundError
            await session.bookings_repository.delete(id=booking_id, user_id=user.id)
            return {"message": "Бронь успешно удалена", "reservation_id": booking_id}
