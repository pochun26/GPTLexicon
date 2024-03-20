from fastapi import APIRouter, HTTPException, Depends
from . import MessageResponse
from sqlalchemy.orm import Session
from app.cards import crud, models, schemas
from app.database import engine
from app.dependencies import get_db
import datetime

models.Base.metadata.create_all(bind=engine)


router = APIRouter(prefix="/card",
                   tags=["card"],
                   responses={404: {"model": MessageResponse}})


@router.get("s")
async def get_cards(db: Session = Depends(get_db)) -> list[schemas.CardSchema]:
    return crud.get_due_cards(db)


@router.post("/")
async def create_card(card: schemas.CardSchemaBase, db: Session = Depends(get_db)):
    db_card = crud.get_card(db, card.word)
    if db_card:
        raise HTTPException(status_code=400, detail="Card already exists")

    return crud.create_card(db, card)


@router.put("/")
async def update_card(card: schemas.CardSchema, db: Session = Depends(get_db)) -> schemas.CardSchema:
    db_card = crud.get_card(db, card.word)
    if db_card is None:
        raise HTTPException(status_code=404, detail="Card not found")

    return crud.update_card(db, card)


@router.get("/{word}")
async def get_card(word: str, db: Session = Depends(get_db)) -> schemas.CardSchema:
    db_card = crud.get_card(db, word)
    if db_card is None:
        raise HTTPException(status_code=404, detail="Card not found")
    return db_card


@router.delete("/{word}")
async def delete_card(word: str, db: Session = Depends(get_db)) -> schemas.CardSchema:
    db_card = crud.get_card(db, word)
    if db_card is None:
        raise HTTPException(status_code=404, detail="Card not found")
    return crud.delete_card(db, word)


@router.put("/review")
async def review_card(review: schemas.UpdateInterval, db: Session = Depends(get_db)) -> schemas.CardSchema:
    db_card = crud.get_card(db, review.word)
    if db_card is None:
        raise HTTPException(status_code=404, detail="Card not found")

    quality = review.quality

    # calculate new interval
    if quality >= 3:
        if db_card.repetitions == 0:
            db_card.interval = 1
        elif db_card.repetitions == 1:
            db_card.interval = 6
        else:
            db_card.interval *= db_card.efactor
        db_card.repetitions += 1
    else:
        db_card.interval = 1
        db_card.repetitions = 0
    
    db_card.efactor = round(db_card.efactor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02)), 3)
    if db_card.efactor < 1.3:
        db_card.efactor = 1.3

    db_card.next_review = datetime.datetime.now() + datetime.timedelta(days=db_card.interval)

    return crud.update_card(db, db_card)
