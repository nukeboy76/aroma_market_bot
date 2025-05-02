"""
Точка входа бота «Арома Маркет».
aiogram ≥ 3.18
"""

import asyncio
import logging
from contextlib import suppress

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand

from app.config import settings
from app.handlers.common import router as common_router
from app.handlers.catalog import router as catalog_router
from app.handlers.loyalty import router as loyalty_router
from app.handlers.order import router as order_router
from app.middlewares.db_session import DbSessionMiddleware


async def set_commands(bot: Bot) -> None:
    """Устанавливаем команды бота, видимые в меню Telegram."""
    commands = [
        BotCommand(command="start",   description="Запустить бота"),
        BotCommand(command="catalog", description="Открыть каталог"),
        BotCommand(command="card",    description="Моя карта лояльности"),
        BotCommand(command="order",   description="Моя корзина"),
        BotCommand(command="help",    description="Справка"),
    ]
    await bot.set_my_commands(commands)


def create_dispatcher() -> Dispatcher:
    """Создаём Dispatcher, регистрируем middleware и роутеры."""
    dp = Dispatcher()

    # global middleware
    dp.update.middleware(DbSessionMiddleware())

    # подключаем роутеры
    dp.include_router(common_router)
    dp.include_router(catalog_router)
    dp.include_router(loyalty_router)
    dp.include_router(order_router)

    return dp


async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )

    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    dp = create_dispatcher()

    # до старта поллинга
    await set_commands(bot)

    # запускаем лонг-поллинг
    await dp.start_polling(
        bot, 
        allowed_updates=dp.resolve_used_update_types()
    )

    # закрываем сессию aiohttp
    await bot.session.close()


if __name__ == "__main__":
    with suppress(KeyboardInterrupt, SystemExit):
        asyncio.run(main())
