from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.product import Product


class OrderService:
    """Сервис оформления и получения заказов."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(
        self,
        user_id: int,
        items: dict[int, int],  # product_id -> quantity
    ) -> Order:
        """Создать новый заказ и вернуть его."""
        products = (
            await self.session.scalars(
                select(Product).where(Product.id.in_(items.keys()))
            )
        ).all()

        total_price = sum(p.price * items[p.id] for p in products)
        order = Order(user_id=user_id, total_price=total_price)

        for product in products:
            order.items.append(
                OrderItem(product_id=product.id, quantity=items[product.id])
            )

        self.session.add(order)
        await self.session.commit()
        await self.session.refresh(order)
        return order

    async def list_by_user(self, user_id: int) -> list[Order]:
        """Вернуть все заказы пользователя, отсортированные по дате."""
        stmt = (
            select(Order)
            .where(Order.user_id == user_id)
            .order_by(Order.created_at.desc())
        )
        return (await self.session.scalars(stmt)).all()
