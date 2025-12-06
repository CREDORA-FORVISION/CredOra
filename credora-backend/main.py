from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from db import Base, engine
from models_db import *  # noqa
from routers import auth, ml, reports, banker

# Create tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(title="CredOra Backend API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # for dev; for deploy, restrict to your frontend origin
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
