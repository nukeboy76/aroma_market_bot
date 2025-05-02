from pydantic import BaseModel


class UserRead(BaseModel):
    id: int
    telegram_id: int
    loyalty_points: int

    class Config:
        from_attributes = True
