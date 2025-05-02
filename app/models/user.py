from sqlalchemy import BigInteger, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class User(Base):
    """Модель пользователя Telegram с лояльностью."""

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
    first_name: Mapped[str | None] = mapped_column(String(60), nullable=True)
    loyalty_points: Mapped[int] = mapped_column(Integer, default=0, init=False)

    orders: Mapped[list["Order"]] = relationship(
        "Order",
        back_populates="user",
        lazy="selectin",
        init=False,
    )