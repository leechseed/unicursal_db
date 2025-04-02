from fastapi import FastAPI
from app import models
from app.database import engine
from app.routers import users

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router)

@app.get("/")
def read_root():
    return {"message": "UnicursalDB app is alive"}
