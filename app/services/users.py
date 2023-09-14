from app.interfaces.unit_of_work import IUnitOfWork


class UsersServices:
    def __init__(self, unit_of_work: IUnitOfWork):
        self.unit_of_work = unit_of_work

    @staticmethod
    def read_users_me(current_user):
        return current_user
