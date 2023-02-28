from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from project.config import POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_PORT, POSTGRES_DB, DATABASE_URI


# Make sense to refactor it and put in core package

SQLALCHEMY_DATABASE_URL = DATABASE_URI

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Покдлючаем SQLalchemy (up)
