from datetime import date

from sqlalchemy import select, between, or_, insert

from app.database import async_session_maker
from app.dao.base import BaseDAO
from app.bookings.models import Bookings
from app.users.models import Users
from app.hotels.rooms.models import Rooms
from app.exceptions import RoomFullyBooked


class BookingDAO(BaseDAO):
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
    async def add(cls, room_id: int, date_from: date, date_to: date, user: Users):
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
                add_booking = insert(Bookings).values(room_id=room_id, user_id=user.id, date_from=date_from,
                                                      date_to=date_to, price=price).returning(Bookings)

                new_booking = await session.execute(add_booking)
                await session.commit()
                return new_booking.scalars().first()
            else:
                raise RoomFullyBooked
