from typing import Any, AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import  declarative_base
from .config import settings

Base = declarative_base()


engine= create_async_engine(url=settings.DATABASE_URL, echo=False )

SessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_db() -> AsyncGenerator[AsyncSession | Any, Any]:
    async with SessionLocal() as conn:
        yield conn