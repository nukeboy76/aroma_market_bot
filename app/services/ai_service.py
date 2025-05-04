import logging

from ollama import chat
from ollama import ChatResponse

from app.config import settings

class AIService:
    """Сервис общения с OpenAI для ответов о продуктах."""

    @staticmethod
    async def answer_about_product(product: dict, question: str) -> str:
        prompt = (
            f"Товар: {product['name']} ({product['category']}, {product['country']}).\n"
            f"Описание: {product.get('description', '(нет описания)')}\n"
            f"Цена: {product['price'] / 100:.2f} ₽\n\n"
            f"Вопрос пользователя: {question}\n"
            f"Вежливый и краткий ответ:"
        )

        logging.info(prompt)

        response: ChatResponse = chat(
            model="gemma3:12b",
            messages=[
                {"role": "system", "content": "Вы — помощник магазина Aroma Market."},
                {"role": "user",   "content": prompt},
            ],
        )

        return response.message.content
