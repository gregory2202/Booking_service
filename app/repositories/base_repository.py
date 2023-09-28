from sqlalchemy import delete, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.interfaces.repository import IRepository


class SQLAlchemyBaseRepository(IRepository):
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def find_all(self, **kwargs):
        query = select(self.model).filter_by(**kwargs)
        result = await self.session.execute(query)
        return result.mappings().all()

    async def find_one_or_none(self, **kwargs):
        query = select(self.model).filter_by(**kwargs)
        result = await self.session.execute(query)
        return result.scalars().first()

    async def add(self, **kwargs):
        query = insert(self.model).values(**kwargs).returning(self.model)
        result = await self.session.execute(query)
        return result.mappings().first()

    async def delete(self, **kwargs):
        query = delete(self.model).filter_by(**kwargs)
        await self.session.execute(query)
