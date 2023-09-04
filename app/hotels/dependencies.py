from app.hotels.repository import HotelsRepository
from app.hotels.services import HotelsServices


def get_hotels_services():
    return HotelsServices(HotelsRepository)
