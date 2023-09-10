from app.models.users import Users
from app.repositories.base_repository import SQLAlchemyRepository


class UsersRepositoryAbstract(SQLAlchemyRepository):
    model = Users
