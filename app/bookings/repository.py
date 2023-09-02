from datetime import date

from sqlalchemy import select, between, or_, insert

from app.database import async_session_maker
from app.repository.base_repository import SQLAlchemyRepository
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from app.bookings.models import Bookings
from app.users.models import Users
from app.exceptions import RoomFullyBooked


class BookingsRepository(SQLAlchemyRepository):
    model = Bookings

    @classmethod
    async def find_all_with_images(cls, user_id: int):
        """
        SELECT bookings.*, rooms.*
        FROM bookings JOIN rooms ON bookings.room_id = rooms.id
        WHERE bookings.user_id = [number]
        """

        query = select(Bookings.__table__.columns, Rooms.__table__.columns) \
            .join(Rooms).where(Bookings.user_id == user_id)

        async with async_session_maker() as session:
            bookings = await session.execute(query)
            return bookings.mappings().all()

    @classmethod
    async def add(cls, user_id: int, room_id: int, date_from: date, date_to: date):
        """
        SELECT rooms.quantity
        FROM rooms
        WHERE rooms.id = [room_id];

        SELECT count(*)
        FROM rooms
        WHERE room_id = [room_id]
                    AND (bookings.date_from BETWEEN '2023-06-10' AND '2023-06-10'
                    OR '2023-06-10' BETWEEN bookings.date_from AND bookings.date_to)
        """

        get_rooms_quantity = select(Rooms.quantity).where(Rooms.id == room_id)

        get_booked_rooms = select(Bookings).where(Bookings.room_id == room_id).where(
            or_(between(Bookings.date_from, date_from, date_to),
                between(date_from, Bookings.date_from, Bookings.date_to)))

        async with async_session_maker() as session:
            rooms_quantity = await session.execute(get_rooms_quantity)
            booked_rooms = await session.execute(get_booked_rooms)
            rooms_left = rooms_quantity.scalar() - len(booked_rooms.mappings().all())

            if rooms_left > 0:
                get_price = select(Rooms.price).where(Rooms.id == room_id)
                price = await session.execute(get_price)
                price = price.scalar()
                add_booking = insert(Bookings).values(room_id=room_id, user_id=user_id, date_from=date_from,
                                                      date_to=date_to, price=price).returning(Bookings)

                new_booking = await session.execute(add_booking)
                await session.commit()
                return new_booking.scalars().first()
            else:
                raise RoomFullyBooked

    @classmethod
    async def find_data_for_mail(cls, booking: Bookings):
        """
        SELECT bookings.date_from, bookings.date_to, bookings.total_cost, users.email, hotels.name, rooms.name
        FROM bookings
                JOIN users ON bookings.user_id = users.id
                JOIN rooms ON bookings.room_id = rooms.id
                JOIN hotels ON rooms.hotel_id = hotels.id
        WHERE bookings.id = [booking_id]
        """

        query = select(Bookings.date_from, Bookings.date_to, Bookings.total_cost, Users.email,
                       Hotels.name.label("hotel_name"), Rooms.name.label("room_name")).where(Bookings.id == booking.id)

        async with async_session_maker() as session:
            data_for_email = await session.execute(query)
        return data_for_email.mappings().first()
