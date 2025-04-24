from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from datetime import date


import models


def get_firm(db: Session, firm_id: int):
    return db.query(models.Firm).filter(
        models.Firm.firm_id == firm_id).first()


def get_firms(db: Session, skip: int = 0, limit: int = 100,
               min_last_changed_date: date = None,
               firm_name : str = None, ):
    #  eager loading, which causes SQLAlchemy to retrieve the joined vote data when it retrieves the firm data.
   query = db.query(models.Firm
                   ).options(joinedload(models.Firm.votes))
   if min_last_changed_date:
       query = query.filter(
           models.Firm.last_changed_date >= min_last_changed_date)
   if firm_name:
       query = query.filter(models.Firm.firm_name == firm_name)
   return query.offset(skip).limit(limit).all()


def get_reports(db: Session, skip: int = 0, limit: int = 100,
                    min_last_changed_date: date = None):
   query = db.query(models.Report)
   if min_last_changed_date:
       query = query.filter(
           models.Report.last_changed_date >= min_last_changed_date)
   return query.offset(skip).limit(limit).all()


def get_user(db: Session, user_id: int = None):
   return db.query(models.User).filter(
       models.User.user_id == user_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 100,
                min_last_changed_date: date = None, email: str = None):
   
   if min_last_changed_date:
       query = query.filter(
           models.User.last_changed_date >= min_last_changed_date)                             
   if email:
       query = query.filter(models.User.email == email)    
   return query.offset(skip).limit(limit).all()


def get_votes(db: Session, skip: int = 0, limit: int = 100,
             min_last_changed_date: date = None,
             user_id: str = None, firm_id: int = None):
   query = db.query(models.Vote)
   if min_last_changed_date:
       query = query.filter(
           models.Vote.last_changed_date >= min_last_changed_date)
   if user_id:
       query = query.filter(models.Vote.user_id == user_id)
   if firm_id:
       query = query.filter(models.Vote.firm_id == firm_id)
   return query.offset(skip).limit(limit).all()   


#analytics queries
def get_firm_count(db: Session):
   query = db.query(models.Firm)
   return query.count()


def get_user_count(db: Session):
   query = db.query(models.User)
   return query.count()


def get_vote_count(db: Session):
   query = db.query(models.Vote)
   return query.count()