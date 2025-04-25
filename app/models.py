from sqlalchemy import Column, Integer, Float, String, Boolean, ForeignKey, DateTime, Date
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship
from .database import Base


class Firm(Base):
    __tablename__ = "firm"

    firm_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    firm_name = Column(String, nullable=False)
    licenced = Column(Boolean, server_default='TRUE', nullable=False)
    last_changed_date = Column(Date, nullable=False)

    reports = relationship("Report", back_populates="firm")
    # Many-to-many relationship between Firm and User tables
    votes = relationship("User", secondary="vote", back_populates="vote")

    # created_at = Column(DateTime(timezone=True), nullable=False, server_default=text('func.now()'))
    # owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    # owner = relationship("User", back_populates="id")


class Report(Base):
    __tablename__ = "report"

    report_id = Column(Integer, primary_key=True, index=True)
    week_number = Column(String, nullable=False)
    firm_rate = Column(Float, nullable=False)
    last_changed_date = Column(Date, nullable=False)
    firm_id = Column(Integer, ForeignKey("firm.firm_id"))

    firm = relationship("Firm", back_populates="reports")

class User(Base):
    __tablename__ = "user"
    
    user_id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    last_changed_date = Column(Date, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=text('func.now()'))

    # Many-to-many relationship between User and Firm tables
    vote = relationship("Firm", secondary="vote", back_populates="votes")


class Vote(Base):
    __tablename__ = "vote"
    
    user_id = Column(Integer, ForeignKey("user.user_id", ondelete="CASCADE"), primary_key=True, index=True)
    firm_id = Column(Integer, ForeignKey("firm.firm_id", ondelete="CASCADE"), primary_key=True, index=True)
    last_changed_date = Column(Date, nullable=False)
