from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


from project.db.db import Base


# Model for User
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

    company = relationship("Company", back_populates="user")


users = User.__table__


# Model for Company
class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer, primary_key=True, index=True, unique=True)
    name = Column(String(30), unique=True)
    description = Column(String(100))
    owner_id = Column(Integer, ForeignKey('users.id'))
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="company")


companies = Company.__table__
