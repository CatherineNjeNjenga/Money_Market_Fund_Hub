from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship
from .database import Base


class Firm(Base):
    __tablename__ = 'firms'

    code = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    fund_manager = Column(String, nullable=False)
    week_1 = Column(String, nullable=False)
    week_2 = Column(String, nullable=False)
    week_3 = Column(String, nullable=False)
    week_4 = Column(String, nullable=False)
    week_5 = Column(String, nullable=False)
    week_6 = Column(String, nullable=False)
    week_7 = Column(String, nullable=False)
    week_8 = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("User")
    licenced = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=text('func.now()'))

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=text('func.now()'))


class Vote(Base):
    __tablename__ = "votes"
    
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    firm_id = Column(Integer, ForeignKey("firms.code", ondelete="CASCADE"), primary_key=True)