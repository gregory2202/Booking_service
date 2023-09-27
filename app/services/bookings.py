from app.exceptions.exceptions import RoomCannotBeBooked, ReservationNotFoundError, InvalidDateError, \
    ExcessiveBookingDurationError, RoomNotFoundError
from app.interfaces.unit_of_work import IUnitOfWork
from app.models.users import Users
from app.schemas.bookings import SNewBooking


class BookingsServices:
    def __init__(self, unit_of_work: IUnitOfWork):
        self.unit_of_work = unit_of_work

    async def get_bookings(self, user: Users):
        async with self.unit_of_work as uow:
            return await uow.bookings_repository.find_all_with_images(user_id=user.id)

    async def add_booking(self, booking: SNewBooking, user: Users):
        if booking.date_from > booking.date_to:
            raise InvalidDateError
        if (booking.date_to - booking.date_from).days > 30:
            raise ExcessiveBookingDurationError

        async with self.unit_of_work as uow:
            if not await uow.rooms_repository.find_one_or_none(id=booking.room_id):
                raise RoomNotFoundError

            booking = await uow.bookings_repository.add(user_id=user.id, room_id=booking.room_id,
                                                        date_from=booking.date_from,
                                                        date_to=booking.date_to)
            if not booking:
                raise RoomCannotBeBooked
            return booking

    async def remove_booking(self, booking_id: int, user: Users):
        async with self.unit_of_work as uow:
            booking = await uow.bookings_repository.find_one_or_none(id=booking_id, user_id=user.id)
            if not booking:
                raise ReservationNotFoundError
            await uow.bookings_repository.delete(id=booking_id, user_id=user.id)
            return {"message": "Бронь успешно удалена", "reservation_id": booking_id}
