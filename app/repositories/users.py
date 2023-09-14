from app.interfaces.repository import IUsersRepository
from app.models.users import Users
from app.repositories.base_repository import SQLAlchemyBaseRepository


class SQLAlchemyUsersRepository(SQLAlchemyBaseRepository, IUsersRepository):
    model = Users
