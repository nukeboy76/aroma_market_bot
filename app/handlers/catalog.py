from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from app.schemas.product import ProductRead
from app.services.product_service import ProductService
from app.services.ai_service import AIService


router = Router(name="catalog")


# ---------- главное меню ---------------------------------------------- #


def main_menu_keyboard() -> types.ReplyKeyboardMarkup:
    kb = [
        [types.KeyboardButton(text="Каталог")],
        [types.KeyboardButton(text="Лояльная карта")],
        [types.KeyboardButton(text="Корзина")],
    ]
    return types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)


# ---------- список категорий ------------------------------------------ #


async def _send_categories(msg: types.Message | types.CallbackQuery, session, state: FSMContext):
    # Clear any previous product context
    await state.clear()  # reset current_product_id
    svc = ProductService(session)
    cats = await svc.get_categories()

    kb = [
        [types.InlineKeyboardButton(text=cat, callback_data=f"cat:{cat}")]
        for cat in cats
    ]

    text = "Выберите категорию:"
    inline = types.InlineKeyboardMarkup(inline_keyboard=kb)

    if isinstance(msg, types.CallbackQuery):
        await msg.message.edit_text(text, reply_markup=inline)
        await msg.answer()
    else:
        await msg.answer(text, reply_markup=inline)


@router.message(Command("catalog"))
@router.message(lambda m: m.text == "Каталог")
async def show_categories(message: types.Message, session, state: FSMContext) -> None:
    await _send_categories(message, session, state)


@router.callback_query(lambda c: c.data == "categories")
async def back_to_categories(query: types.CallbackQuery, session, state: FSMContext) -> None:
    await _send_categories(query, session, state)


@router.callback_query(lambda c: c.data == "main_menu")
async def back_to_main_menu(query: types.CallbackQuery) -> None:
    await query.message.edit_text(
        "<b>Главное меню</b>\nВыберите действие:",
        reply_markup=main_menu_keyboard(),
        parse_mode="HTML",
    )
    await query.answer()


# ---------- список товаров в категории -------------------------------- #


@router.callback_query(lambda c: c.data.startswith("cat:"))
async def choose_category(
    query: types.CallbackQuery, session, state: FSMContext
) -> None:
    await state.clear()  # ensure no leftover product context
    category = query.data.split(":", 1)[1]
    svc = ProductService(session)
    products = await svc.get_by_category(category)

    kb = [
        [types.InlineKeyboardButton(text=p.name, callback_data=f"prod:{p.id}")]
        for p in products
    ]
    kb.append(
        [types.InlineKeyboardButton(text="<< Назад к категориям", callback_data="categories")]
    )

    await query.message.edit_text(
        f"Категория: <b>{category.title()}</b>\n"
        "Выберите товар для подробностей:",
        reply_markup=types.InlineKeyboardMarkup(inline_keyboard=kb),
        parse_mode="HTML",
    )
    await query.answer()


# ---------- карточка товара (редактируем то же сообщение) ------------- #


@router.callback_query(lambda c: c.data.startswith("prod:"))
async def product_details(
    query: types.CallbackQuery, session, state: FSMContext  # 2. Add state here
) -> None:
    product_id = int(query.data.split(":", 1)[1])

    svc = ProductService(session)
    p = await svc.get(product_id)
    dto = ProductRead.model_validate(p)

    await state.update_data(current_product_id=product_id)

    text = f"""<b>{dto.name}</b>
{dto.country}{' | ' + dto.grape if dto.grape else ''}
Цена: {dto.price} ₽
{dto.description or ''}\n
<a href="{dto.post_url}">Вопросы и отзывы</a>"""

    kb = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text="Добавить в заказ", callback_data=f"add:{p.id}"
                )
            ],
            [
                types.InlineKeyboardButton(
                    text="<< Назад к списку", callback_data=f"cat:{p.category}"
                )
            ],
        ]
    )

    await query.message.edit_text(text, reply_markup=kb, parse_mode="HTML")
    await query.answer()

# --------------------------------------------------------------------- #
# Вопросы о товаре
# --------------------------------------------------------------------- #
@router.message(lambda m: m.text and not m.text.startswith("/"))
async def ask_about_product(
    message: types.Message, session, state: FSMContext
) -> None:
    data = await state.get_data()
    product_id = data.get("current_product_id")

    if not product_id:
        await message.answer(
            "Чтобы задать вопрос о товаре, перейдите в любой из "
            "интересующих товаров. Затем задайте вопрос."
        )
        return

    # Отправляем уведомление об обработке
    processing_msg = await message.answer("Ваш вопрос в обработке…")

    # Получаем данные товара
    svc = ProductService(session)
    p = await svc.get(product_id)
    dto = ProductRead.model_validate(p)
    question = message.text.strip()

    # Запрашиваем ответ у OpenAI
    answer = await AIService.answer_about_product(
        product=dto.model_dump(), question=question
    )

    # Редактируем «обрабатываем» на финальный ответ
    await processing_msg.edit_text(answer)