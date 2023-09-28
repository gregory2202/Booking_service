from datetime import date

from sqlalchemy import between, func, or_, select

from app.interfaces.repository import IHotelsRepository
from app.models.bookings import Bookings
from app.models.hotels import Hotels
from app.models.rooms import Rooms
from app.repositories.base_repository import SQLAlchemyBaseRepository


class SQLAlchemyHotelsRepository(SQLAlchemyBaseRepository, IHotelsRepository):
    model = Hotels

    async def find_all(self, location: str, date_from: date, date_to: date):
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

        get_hotels = await self.session.execute(query)
        return get_hotels.mappings().all()
