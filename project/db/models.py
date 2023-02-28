from sqlalchemy import Column, String, Integer, DateTime, Boolean
from sqlalchemy.sql import func


from project.db.db import Base


# can add types in is_root by sqlalchemy_utils
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True, unique=True)
    username = Column(String(30))
    email = Column(String, unique=True)
    hash_password = Column(String, nullable=False)
    is_root = Column(Boolean, default=False)
    status = Column(String, nullable=True)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())