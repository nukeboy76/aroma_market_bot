from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Product(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True)
    category: Mapped[str] = mapped_column(String(60))
    country: Mapped[str] = mapped_column(String(60))
    grape: Mapped[str | None] = mapped_column(String(60), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    price: Mapped[int] = mapped_column()  # в копейках для точности
    image_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
