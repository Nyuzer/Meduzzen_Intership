from sqlalchemy.ext.declarative import declarative_base

from project.config import DATABASE_URI


# Make sense to refactor it and put in core package

SQLALCHEMY_DATABASE_URL = DATABASE_URI


Base = declarative_base()

# Покдлючаем SQLalchemy (up)
