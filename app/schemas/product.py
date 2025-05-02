from pydantic import BaseModel, HttpUrl, field_validator


class ProductRead(BaseModel):
    id: int
    name: str
    category: str
    country: str
    grape: str | None
    description: str | None
    price: int
    image_url: HttpUrl | None

    class Config:
        from_attributes = True

    @field_validator("price", mode="before")
    def cents_to_rubles(cls, v: int) -> float:  # noqa: N802
        return round(v / 100, 2)
