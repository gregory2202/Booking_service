from abc import ABC, abstractmethod

from sqlalchemy import select, insert, delete

from app.database import async_session_maker


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


class SQLAlchemyRepository(AbstractRepository):
    model = None

    @classmethod
    async def find_all(cls, **kwargs):
        query = select(cls.model).filter_by(**kwargs)
        async with async_session_maker() as session:
            result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def find_one_or_none(cls, **kwargs):
        query = select(cls.model).filter_by(**kwargs)
        async with async_session_maker() as session:
            result = await session.execute(query)
            return result.scalars().first()

    @classmethod
    async def add(cls, **kwargs):
        query = insert(cls.model).values(**kwargs).returning(cls.model)
        async with async_session_maker() as session:
            result = await session.execute(query)
            await session.commit()
            return result.mappings().first()

    @classmethod
    async def delete(cls, **kwargs):
        query = delete(cls.model).filter_by(**kwargs)
        async with async_session_maker() as session:
            await session.execute(query)
            await session.commit()
