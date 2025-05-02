from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


class LoyaltyService:
    """Сервис работы с бонусной картой."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    # ---------- utils -------------------------------------------------- #

    async def get_or_create(self, telegram_id: int, first_name: str | None) -> User:
        stmt = select(User).where(User.telegram_id == telegram_id)
        user = await self.session.scalar(stmt)
        if user:
            return user

        user = User(telegram_id=telegram_id, first_name=first_name or "")
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    # ---------- начисление / списание ---------------------------------- #

    async def add_points(self, user: User, amount: int) -> None:
        """Начислить баллы (1 балл = 1 ₽)."""
        user.loyalty_points += amount
        await self.session.commit()

    async def redeem_points(self, user: User, amount: int) -> int:
        """
        Списать до `amount` баллов.  
        Возвращает фактически списанное число.
        """
        used = min(user.loyalty_points, amount)
        user.loyalty_points -= used
        await self.session.commit()
        return used
