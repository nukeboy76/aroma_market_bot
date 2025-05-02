from __future__ import annotations

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class OrderItem(Base):
    """Позиция внутри заказа (товар + количество)."""

    __tablename__ = "order_item"
    __table_args__ = (UniqueConstraint("order_id", "product_id"),)

    # ------------------------------------------------------------------ #
    # Колонки
    # ------------------------------------------------------------------ #

    id: Mapped[int] = mapped_column(primary_key=True, init=False)

    # Задаётся автоматически при добавлении в order.items — не участвует в __init__
    order_id: Mapped[int] = mapped_column(
        ForeignKey("order.id", ondelete="CASCADE"),
        init=False,
    )

    # product_id передаём в конструктор, поэтому оставить init по умолчанию (=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("product.id"))

    quantity: Mapped[int] = mapped_column(default=1)

    # ------------------------------------------------------------------ #
    # Связи
    # ------------------------------------------------------------------ #

    # обратная ссылка на заказ
    order: Mapped["Order"] = relationship(
        "Order",
        back_populates="items",
        init=False,
    )

    # связанный товар; не передаётся в __init__
    product: Mapped["Product"] = relationship(
        "Product",
        init=False,
    )
