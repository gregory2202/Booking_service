from app.interfaces.repository import SQLAlchemyRepository
from app.models.users import Users


class UsersRepository(SQLAlchemyRepository):
    model = Users
