from aiogram import Router, types
from aiogram.filters import CommandStart, Command

router = Router(name="common")


@router.message(CommandStart())
async def cmd_start(message: types.Message) -> None:
    text = (
        "<b>Добро пожаловать в Aroma Market!</b>\n\n"
        "Используйте кнопки ниже или команды для навигации:\n"
        "/catalog — открыть каталог товаров\n"
        "/card    — показать информацию о карте лояльности\n"
        "/order   — отобразить текущий заказ\n"
        "/help    — показать эту справку"
    )
    kb = [
        [types.KeyboardButton(text="Каталог")],
        [types.KeyboardButton(text="Лояльная карта")],
        [types.KeyboardButton(text="Корзина")],
    ]
    await message.answer(
        text,
        reply_markup=types.ReplyKeyboardMarkup(
            keyboard=kb, resize_keyboard=True
        ),
    )


@router.message(Command("help"))
async def cmd_help(message: types.Message) -> None:
    """Справка по доступным командам бота."""
    help_text = (
        "<b>Справка по боту Aroma Market:</b>\n"
        "/start   — перезапустить бота\n"
        "/catalog — открыть каталог товаров\n"
        "/card    — показать информацию о карте лояльности\n"
        "/order   — отобразить текущий заказ\n"
        "/help    — показать эту справку"
    )
    await message.answer(help_text)
