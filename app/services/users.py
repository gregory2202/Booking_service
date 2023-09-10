from app.repositories.users import UsersRepository


class UsersServices:
    def __init__(self, users_repository: UsersRepository):
        self.users_repository = users_repository

    @staticmethod
    def read_users_me(current_user):
        return current_user
