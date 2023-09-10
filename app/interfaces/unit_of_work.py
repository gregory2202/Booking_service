from abc import ABC, abstractmethod


class AbstractUnitOfWork(ABC):

    @abstractmethod
    async def commit(self):
        raise NotImplemented

    @abstractmethod
    async def rollback(self):
        raise NotImplemented


class SQLAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session = self.session_factory()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            await self.rollback()
        else:
            await self.session.commit()
        await self.session.close()
        return False

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
