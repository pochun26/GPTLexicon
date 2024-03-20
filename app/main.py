from fastapi import FastAPI
from .routers import gpt, card


app = FastAPI(title="GPTLexicon")
app.include_router(gpt.router)
app.include_router(card.router)
