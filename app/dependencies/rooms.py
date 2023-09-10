from app.repositories.rooms import RoomsRepositoryAbstract
from app.services.rooms import RoomsServices


def get_rooms_services():
    return RoomsServices(RoomsRepositoryAbstract)
