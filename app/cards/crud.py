from sqlalchemy.orm import Session
from . import models, schemas
from datetime import date


def get_due_cards(db: Session):
    return db.query(models.Card).filter(models.Card.next_review <= date.today()).order_by(models.Card.next_review).all()


def get_card(db: Session, word: str):
    return db.query(models.Card).filter(models.Card.word == word).first()


def delete_card(db: Session, word: int):
    db_card = db.query(models.Card).filter(models.Card.word == word).first()
    db.delete(db_card)
    db.commit()
    return db_card


def create_card(db: Session, card: schemas.CardSchemaBase):
    db_card = models.Card(**card.dict())
    db.add(db_card)
    db.commit()
    db.refresh(db_card)
    return db_card


def update_card(db: Session, card: schemas.CardSchema):
    db_card = db.query(models.Card).filter(
        models.Card.word == card.word).first()
    db_card.interval = card.interval
    db_card.repetitions = card.repetitions
    db_card.efactor = card.efactor
    db_card.next_review = card.next_review
    db.commit()
    db.refresh(db_card)
    return db_card
