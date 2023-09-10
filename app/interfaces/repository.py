from abc import ABC, abstractmethod


class AbstractRepository(ABC):

    @classmethod
    @abstractmethod
    async def find_all(cls, **kwargs):
        raise NotImplemented

    @classmethod
    @abstractmethod
    async def find_one_or_none(cls, **kwargs):
        raise NotImplemented

    @classmethod
    @abstractmethod
    async def add(cls, **kwargs):
        raise NotImplemented

    @classmethod
    @abstractmethod
    async def delete(cls, **kwargs):
        raise NotImplemented


class AbstractSQLAlchemyRepository(AbstractRepository, ABC):
    model = None
