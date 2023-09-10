from pydantic import BaseModel


class SHotel(BaseModel):
    id: int
    name: str
    location: str
    services: list[str]
    rooms_quantity: int
    image_id: int

    class Config:
        from_attributes = True


class SHotelInfo(SHotel):
    rooms_left: int
