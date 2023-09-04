from app.repository.base_repository import SQLAlchemyRepository
from app.users.models import Users


class UsersRepository(SQLAlchemyRepository):
    model = Users
