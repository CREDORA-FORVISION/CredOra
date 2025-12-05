# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import auth, ml, reports, banker
from db import engine
from models_db import Base

app = FastAPI(title="CredOra Backend API")

# Create tables
Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(ml.router)
app.include_router(reports.router)
app.include_router(banker.router)


@app.get("/")
def root():
    return {"message": "CredOra Backend Running"}
