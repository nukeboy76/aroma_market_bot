from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import async_session


class DbSessionMiddleware(BaseMiddleware):
    """Добавляет SQLAlchemy AsyncSession в data-словарь хендлеров."""

    async def __call__(self, handler, event: TelegramObject, data: dict):
        async with async_session() as session:
            data["session"]: AsyncSession = session
            return await handler(event, data)
