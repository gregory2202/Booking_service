from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from app.config import settings

DB_PARAMS = {"poolclass": NullPool} if settings.MODE == "TEST" else {}

engine = create_async_engine(settings.DATABASE_URL, **DB_PARAMS)

async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass
