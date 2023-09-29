from datetime import date

from pydantic import BaseModel, EmailStr


class SEmailConfirmationData(BaseModel):
    date_from: date
    date_to: date
    total_cost: int
    email: EmailStr
    hotel_name: str
    room_name: str
