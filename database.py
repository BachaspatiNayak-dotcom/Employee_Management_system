import os

from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is missing from .env")


# Database engine
engine = create_engine(
    DATABASE_URL,
    echo=True,
    pool_pre_ping=True
)


# Database session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# FastAPI database dependency
def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()