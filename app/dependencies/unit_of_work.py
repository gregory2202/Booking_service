from app.interfaces.unit_of_work import IUnitOfWork
from app.unit_of_work.unit_of_work import SQLAlchemyUnitOfWork


def get_unit_of_work() -> IUnitOfWork:
    return SQLAlchemyUnitOfWork()
