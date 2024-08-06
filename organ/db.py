from typing import AsyncGenerator

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import Session, select

from organ.config import DB_URL, ENVIRONMENT
from organ.models import User


def get_engine(env=ENVIRONMENT):
    return create_engine(DB_URL, echo=True)


# Database session dependency
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


def get_async_engine():
    from sqlalchemy.ext.asyncio import create_async_engine

    return create_async_engine(
        DB_URL.replace('postgresql://', 'postgresql+asyncpg://', 1), echo=True
    )


engine = get_engine()
async_engine = get_async_engine()
async_session = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)
