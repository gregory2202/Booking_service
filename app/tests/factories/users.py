from polyfactory.factories.sqlalchemy_factory import SQLAlchemyFactory

from app.models.users import Users


class UsersFactory(SQLAlchemyFactory[Users]):
    __model__ = Users
