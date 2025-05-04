from aiogram import Router, types
from sqlalchemy import select

from app.schemas.product import ProductRead
from app.services.product_service import ProductService
from app.services.ai_service import AIService

router = Router(name="comments")


@router.channel_post()
async def on_channel_post(post: types.Message, session) -> None:
    thread_id = post.message_thread_id
    if not thread_id:
        return

    title = (post.text or "").splitlines()[0].strip()
    prod = await ProductService(session).get_by_name(title)
    if prod:
        prod.thread_id = thread_id
        await session.commit()


@router.message(lambda m: m.message_thread_id is not None and m.chat.type != "channel")
async def on_comment(msg: types.Message, session) -> None:
    thread_id = msg.message_thread_id
    prod = await ProductService(session).get_by_thread(thread_id)
    if not prod:
        return

    # Конвертация в Pydantic DTO
    dto = ProductRead.model_validate(prod)

    question = msg.text or ""
    answer = await AIService.answer_about_product(
        product=dto.model_dump(),  # теперь dict
        question=question,
    )
    await msg.reply(answer)
