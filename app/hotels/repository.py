from datetime import date

from sqlalchemy import select, func, between, or_

from app.database import async_session_maker
from app.repository.base_repository import SQLAlchemyRepository
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from app.bookings.models import Bookings


class HotelsRepository(SQLAlchemyRepository):
    model = Hotels

    @classmethod
    async def find_all(cls, location: str, date_from: date, date_to: date):
        """
        WITH booked_rooms as (SELECT bookings.room_id, count(*) as booked_rooms
                       FROM bookings
                       WHERE Bookings.date_from between '2023-06-10' and '2023-06-30'
                          or '2023-06-10' between Bookings.date_from and Bookings.date_to
                       GROUP BY bookings.room_id)

        SELECT hotels.*, hotels.rooms_quantity - SUM(coalesce(booked_rooms, 0)) as room_left
        FROM hotels
                 LEFT JOIN rooms ON hotels.id = rooms.hotel_id
                 LEFT JOIN booked_rooms ON rooms.id = booked_rooms.room_id
        WHERE hotels.location LIKE '%Алтай%'
        GROUP BY hotels.id, hotels.rooms_quantity
        HAVING hotels.rooms_quantity - SUM(coalesce(booked_rooms, 0)) > 0
        """

        booked_rooms = select(Bookings.room_id, func.count('*').label('booked_rooms')) \
            .where(or_(between(Bookings.date_from, date_from, date_to),
                       between(date_from, Bookings.date_from, Bookings.date_to))) \
            .group_by(Bookings.room_id) \
            .cte('booked_rooms')

        query = select(Hotels.__table__.columns,
                       (Hotels.rooms_quantity - func.sum(func.coalesce(booked_rooms.columns.booked_rooms, 0)))
                       .label('rooms_left')) \
            .join(Rooms, isouter=True) \
            .join(booked_rooms, booked_rooms.columns.room_id == Rooms.id, isouter=True) \
            .where(Hotels.location.like(f'%{location}%')) \
            .group_by(Hotels.id, Hotels.rooms_quantity) \
            .having(Hotels.rooms_quantity - func.sum(func.coalesce(booked_rooms.columns.booked_rooms, 0)) > 0)

        async with async_session_maker() as session:
            get_hotels = await session.execute(query)
            return get_hotels.mappings().all()
