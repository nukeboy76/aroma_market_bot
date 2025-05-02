from __future__ import annotations

from datetime import datetime

from sqlalchemy import ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Order(Base):
    """Заказ пользователя."""

    # ------------------------------------------------------------------ #
    # Колонки
    # ------------------------------------------------------------------ #

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    # total_price передаётся при создании
    total_price: Mapped[int] = mapped_column(Integer)

    # created_at формируется СУБД; не должен попадать в __init__
    created_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow,          # для Python-сессии
        server_default=func.now(),        # для БД
        init=False,
    )

    status: Mapped[str] = mapped_column(String(30), default="new")

    # ------------------------------------------------------------------ #
    # Связи
    # ------------------------------------------------------------------ #

    items: Mapped[list["OrderItem"]] = relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete-orphan",
        lazy="selectin",
        init=False,
        default_factory=list,
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="orders",
        lazy="selectin",
        init=False,
    )
