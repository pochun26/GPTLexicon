from pydantic import BaseModel
import datetime


class CardSchemaBase(BaseModel):
    word: str


class CardSchema(CardSchemaBase):
    id: int
    interval: int
    repetitions: int
    efactor: float
    next_review: datetime.date

    class Config:
        orm_mode = True


class UpdateInterval(BaseModel):
    word: str
    quality: int
