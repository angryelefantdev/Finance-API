
from fastapi import FastAPI

from database import Base, engine
from models import categories, transactions, users

from routers import auth, categories as categories_router
from routers import transactions as transactions_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="finance tracker api")

app.include_router(auth.router)
app.include_router(categories_router.router)
app.include_router(transactions_router.router)


@app.get("/")
def home():
    return {"message": "welcome to finance tracker"}