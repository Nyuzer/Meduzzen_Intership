from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy_utils.types.choice import ChoiceType


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

    company = relationship("Company", secondary="CompanyRequests", back_populates="user")


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

    user = relationship("User", secondary="CompanyRequests", back_populates="company", cascade='all, delete')


companies = Company.__table__


class CompanyMembers(Base):
    TYPES = [
        ('general-user', 'General user'),
        ('owner', 'Owner'),
        ('admin', 'Admin')
    ]

    __tablename__ = 'companies_members'

    id = Column(Integer, primary_key=True, index=True, unique=True)
    company_id = Column(Integer, ForeignKey('companies.id', ondelete='CASCADE'))
    user_id = Column(Integer, ForeignKey('users.id'))
    role = Column(ChoiceType(TYPES))


company_members = CompanyMembers.__table__


class Action(Base):
    TYPES = [
        ('invited', 'Invited to company'),
        ('accession-request', 'Accession request to company')
    ]

    __tablename__ = 'actions'

    id = Column(Integer, primary_key=True, index=True, unique=True)
    company_id = Column(Integer, ForeignKey('companies.id', ondelete='CASCADE'))
    user_id = Column(Integer, ForeignKey('users.id'))
    type_of_request = Column(ChoiceType(TYPES))
    invite_message = Column(String(150), nullable=True)


actions = Action.__table__


class Quizz(Base):
    __tablename__ = 'quizzes'

    id = Column(Integer, primary_key=True, index=True, unique=True)
    name = Column(String(50), nullable=False)
    description = Column(String(150), nullable=False)
    number_of_frequency = Column(Integer)
    author_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    updated_by = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    company_id = Column(Integer, ForeignKey('companies.id', ondelete='CASCADE'))
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    question = relationship('Question', back_populates='quizz')


quizzes = Quizz.__table__


class Question(Base):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True, index=True, unique=True)
    question = Column(String, nullable=False)
    answers = Column(ARRAY(String), nullable=False)
    correct_answer = Column(String, nullable=False)
    quizz_id = Column(Integer, ForeignKey('quizzes.id', ondelete='CASCADE'))

    quizz = relationship('Quizz', back_populates='question')


questions = Question.__table__
