from app.database import Base
from sqlalchemy import Boolean, Column, Integer, Float, String, Date
from datetime import date


class Card(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True, index=True)
    word = Column(String, index=True, unique=True)
    interval = Column(Integer, index=True, default=1)
    repetitions = Column(Integer, index=True, default=0)
    efactor = Column(Float, index=True, default=2.5)
    next_review = Column(Date, index=True, default=date.today())
