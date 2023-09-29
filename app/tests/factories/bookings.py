from polyfactory.factories.pydantic_factory import ModelFactory

from app.schemas.bookings import SNewBooking


class BookingsFactory(ModelFactory[SNewBooking]):
    __model__ = SNewBooking
