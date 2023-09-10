from app.repositories.hotels import HotelsRepositoryAbstract
from app.services.hotels import HotelsServices


def get_hotels_services():
    return HotelsServices(HotelsRepositoryAbstract)
