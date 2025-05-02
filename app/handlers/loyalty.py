from aiogram import Router, types
from aiogram.filters import Command

from app.schemas.user import UserRead
from app.services.loyalty_service import LoyaltyService

router = Router(name="loyalty")

@router.message(Command("card"))
@router.message(lambda m: m.text == "Лояльная карта")
async def loyalty_card(message: types.Message, session) -> None:
    svc = LoyaltyService(session)
    user = await svc.get_or_create(
        telegram_id=message.from_user.id,
        first_name=message.from_user.first_name,
    )
    dto = UserRead.model_validate(user)
    await message.answer(
        f"Ваша карта активна!\n\n"
        f"Накопленные баллы: <b>{dto.loyalty_points}</b>"
    )
