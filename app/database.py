from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.config import settings

engine = create_async_engine(
    settings.database_url,  # postgresql+asyncpg://user:pass@db:5432/aroma
    echo=settings.log_level == "DEBUG",
    future=True,
)

async_session: async_sessionmaker[AsyncSession] = async_sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Асинхронный генератор сессий для FastAPI/aiogram-зависимостей."""
    async with async_session() as session:
        yield session
