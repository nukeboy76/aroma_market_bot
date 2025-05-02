from __future__ import annotations

from aiogram import Router, types
from aiogram.filters import Command
from sqlalchemy import select

from app.models.order import Order
from app.models.product import Product
from app.services.loyalty_service import LoyaltyService
from app.services.order_service import OrderService

router = Router(name="order")

# Памятное хранилище (MVP)
CART: dict[int, dict[int, int]] = {}      # telegram_id -> {product_id: qty}
USE_BONUS: dict[int, bool] = {}           # telegram_id -> True/False


# ---------- добавление товара ----------------------------------------- #


@router.callback_query(lambda c: c.data.startswith("add:"))
async def add_to_cart(query: types.CallbackQuery) -> None:
    product_id = int(query.data.split(":", 1)[1])
    cart = CART.setdefault(query.from_user.id, {})
    cart[product_id] = cart.get(product_id, 0) + 1
    await query.answer("Товар добавлен!")


# ---------- просмотр корзины ------------------------------------------ #


async def _cart_keyboard() -> types.InlineKeyboardMarkup:
    """Клавиатура корзины с выбором действия над бонусами и очисткой."""
    return types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text="Списать бонусы", callback_data="checkout:use"
                ),
                types.InlineKeyboardButton(
                    text="Накопить бонусы", callback_data="checkout:save"
                ),
            ],
            [
                types.InlineKeyboardButton(
                    text="🗑 Очистить корзину", callback_data="cart:clear"
                )
            ],
        ]
    )


@router.message(Command("order"))
@router.message(lambda m: m.text == "Корзина")
async def show_cart(message: types.Message, session) -> None:
    await _render_cart(message, session, edit=False)


# ---------- «очистить корзину» ---------------------------------------- #


@router.callback_query(lambda c: c.data == "cart:clear")
async def clear_cart(query: types.CallbackQuery) -> None:
    CART.pop(query.from_user.id, None)
    USE_BONUS.pop(query.from_user.id, None)
    await query.message.edit_text("Корзина очищена.")
    await query.answer("Готово!")


# ---------- выбор списать / накопить ---------------------------------- #


@router.callback_query(lambda c: c.data.startswith("checkout:"))
async def checkout(query: types.CallbackQuery, session) -> None:
    USE_BONUS[query.from_user.id] = query.data.endswith("use")
    await query.answer()
    await confirm_order(query.message, session, query.from_user.id)


# ---------- оформление заказа ----------------------------------------- #


async def confirm_order(message: types.Message, session, tg_id: int | None = None):
    user_tg_id = tg_id or message.from_user.id
    cart = CART.get(user_tg_id)
    if not cart:
        await message.answer("Ваша корзина пуста.")
        return

    loyalty_svc = LoyaltyService(session)
    user = await loyalty_svc.get_or_create(
        telegram_id=user_tg_id, first_name=message.from_user.first_name
    )
    order_svc = OrderService(session)
    order = await order_svc.create(user_id=user.id, items=cart)

    total_rub = order.total_price // 100
    use_bonus = USE_BONUS.get(user_tg_id, False)

    if use_bonus and user.loyalty_points:
        used = await loyalty_svc.redeem_points(user, total_rub)
        remaining = total_rub - used
        bonus_add = remaining // 10
        await loyalty_svc.add_points(user, bonus_add)

        reply = (
            f"Бонусы списаны: {used}\n"
            f"К оплате осталось: {remaining} ₽\n"
            f"Начислено новых бонусов: {bonus_add}"
        )
        need_payment = remaining > 0
    else:
        bonus_add = total_rub // 10
        await loyalty_svc.add_points(user, bonus_add)
        reply = f"Будет начислено <b>{bonus_add}</b> бонусов."
        need_payment = total_rub > 0

    # очищаем состояние
    CART.pop(user_tg_id, None)
    USE_BONUS.pop(user_tg_id, None)

    kb = (
        types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(
                        text="💳 Оплатить", callback_data=f"pay:{order.id}"
                    )
                ]
            ]
        )
        if need_payment
        else None
    )

    # редактируем исходное бот-сообщение, если можно
    if message.from_user.is_bot:
        await message.edit_text(reply, reply_markup=kb, parse_mode="HTML")
    else:
        await message.answer(reply, reply_markup=kb, parse_mode="HTML")


# ---------- «оплатить» ------------------------------------------------- #


@router.callback_query(lambda c: c.data.startswith("pay:"))
async def pay_order(query: types.CallbackQuery, session) -> None:
    order_id = int(query.data.split(":", 1)[1])
    await session.execute(
        Order.__table__.update().where(Order.id == order_id).values(status="paid")
    )
    await session.commit()
    await query.answer("Заказ оплачен. Спасибо за покупку!", show_alert=True)


# ---------- helpers ---------------------------------------------------- #


async def _render_cart(message: types.Message, session, *, edit: bool) -> None:
    """Вывести/обновить текст корзины (edit=True – редактировать)."""
    cart = CART.get(message.from_user.id)
    if not cart:
        text = "Ваша корзина пуста."
        if edit and message.from_user.is_bot:
            await message.edit_text(text)
        else:
            await message.answer(text)
        return

    product_ids = list(cart.keys())
    result = await session.execute(
        select(Product.id, Product.name).where(Product.id.in_(product_ids))
    )
    names = {row.id: row.name for row in result.all()}

    lines = [
        f"• <b>{names.get(pid, '???')}</b>: {qty} шт."
        for pid, qty in cart.items()
    ]

    loyalty_svc = LoyaltyService(session)
    user = await loyalty_svc.get_or_create(
        telegram_id=message.from_user.id,
        first_name=message.from_user.first_name,
    )

    text = (
        "Ваш заказ:\n"
        + "\n".join(lines)
        + f"\n\n<b>Доступно бонусов:</b> {user.loyalty_points}"
        "\nКак поступить с бонусами?"
    )

    if edit and message.from_user.is_bot:
        await message.edit_text(text, reply_markup=await _cart_keyboard(), parse_mode="HTML")
    else:
        await message.answer(text, reply_markup=await _cart_keyboard(), parse_mode="HTML")
