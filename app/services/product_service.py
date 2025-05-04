from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.product import Product


class ProductService:
    """Логика каталога."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get(self, product_id: int) -> Product:
        return await self.session.get(Product, product_id)

    async def get_categories(self) -> list[str]:
        stmt = select(Product.category).distinct().order_by(Product.category)
        result = await self.session.execute(stmt)
        return [row[0] for row in result.all()]

    async def get_by_category(self, category: str) -> list[Product]:
        stmt = (
            select(Product)
            .where(Product.category == category)
            .order_by(Product.name)
        )
        return (await self.session.scalars(stmt)).all()

    async def get_by_name(self, category: str) -> Product | None:
        stmt = select(Product).where(Product.name == name)
        return await self.session.scalar(stmt)

    async def get_by_thread(self, thread_id: int) -> Product | None:
        stmt = select(Product).where(Product.thread_id == thread_id)
        return await self.session.scalar(stmt)

