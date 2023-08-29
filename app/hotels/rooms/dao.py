from datetime import date

from sqlalchemy import select, func, or_, between

from app.dao.base import BaseDAO
from app.hotels.rooms.models import Rooms
from app.bookings.models import Bookings
from app.database import async_session_maker


class RoomsDAO(BaseDAO):
    model = Rooms

    @classmethod
    async def find_all(cls, hotel_id: int, date_from: date, date_to: date):
        """
        WITH booking_rooms as (
                        SELECT bookings.room_id, count(*) as booked_rooms
                        FROM bookings
                        WHERE Bookings.date_from between '2023-06-10' and '2023-06-30'
                            or '2023-06-10' between Bookings.date_from and Bookings.date_to
                        GROUP BY bookings.room_id
                        )

        SELECT rooms.*,
            rooms.price * [total_days] as total_cost,
            rooms.quantity - coalesce(booking_rooms.booked_rooms, 0) as rooms_left
        FROM rooms
                 LEFT JOIN booking_rooms ON rooms.id = booking_rooms.room_id
        WHERE rooms.hotel_id = [hotel_id]
        """

        booked_rooms = select(Bookings.room_id, func.count('*').label('booked_rooms')) \
            .where(or_(between(Bookings.date_from, date_from, date_to),
                       between(date_from, Bookings.date_from, Bookings.date_to))) \
            .group_by(Bookings.room_id) \
            .cte('booked_rooms')

        query = select(Rooms.__table__.columns,
                       (Rooms.price * (date_to - date_from).days).label('total_cost'),
                       (Rooms.quantity - func.coalesce(booked_rooms.columns.booked_rooms, 0)).label('rooms_left')) \
            .join(booked_rooms, Rooms.id == booked_rooms.columns.room_id, isouter=True) \
            .where(Rooms.hotel_id == hotel_id)

        async with async_session_maker() as session:
            rooms = await session.execute(query)
            return rooms.mappings().all()
