# db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLite file in project root
SQLALCHEMY_DATABASE_URL = "sqlite:///./credora.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},  # needed for SQLite + FastAPI
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency for FastAPI routes
def get_db():
    from fastapi import Depends

    def _get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    return Depends(_get_db)
