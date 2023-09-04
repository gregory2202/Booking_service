from app.hotels.rooms.repository import RoomsRepository
from app.hotels.rooms.services import RoomsServices


def get_rooms_services():
    return RoomsServices(RoomsRepository)
