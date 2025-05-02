from datetime import datetime

from pydantic import BaseModel, field_validator

from app.schemas.product import ProductRead


class OrderItemRead(BaseModel):
    product: ProductRead
    quantity: int

    class Config:
        from_attributes = True


class OrderRead(BaseModel):
    id: int
    created_at: datetime
    status: str
    total_price: int
    items: list[OrderItemRead]

    @field_validator("total_price", mode="before")
    def cents_to_rubles(cls, v: int) -> float:  # noqa: N802
        return round(v / 100, 2)

    class Config:
        from_attributes = True
