from datetime import date

from pydantic import BaseModel, ConfigDict


class SBooking(BaseModel):
    id: int
    room_id: int
    user_id: int
    date_from: date
    date_to: date
    price: int
    total_cost: int
    total_days: int

    model_config = ConfigDict(from_attributes=True)


class SBookingInfo(SBooking):
    image_id: int
    name: str
    description: str
    services: list[str]


class SNewBooking(BaseModel):
    room_id: int
    date_from: date
    date_to: date


class SDeleteBooking(BaseModel):
    message: str
    reservation_id: int
