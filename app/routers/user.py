from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from .. import models, schemas, utils
from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # hash the password - user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id: {id} doesn't exist")
    return user

@router.get("/", response_model=List[schemas.UserOut]) # FirmOut
def read_users(db: Session = Depends(get_db),
#current_user: int = Depends(oauth2.get_current_user),
              skip: int = Query(0, description="The number of items to skip at the beginning of API call."), 
              limit: int = Query(10, description="The number of records to return after the skipped records."),
              search: Optional[str] = "",
              minimum_last_changed_date: date = Query(None, description="The minimum date of change that you want to return records. Exclude any records changed before this."), 
              firm_name: str = Query(None, description="The name of the firms to return")):
    # sqlite
    # cursor.execute("""SELECT * FROM firms""")
    # firms = cursor.fetchall()

    # sqlalchemy
    # firms = db.query(models.Firm).filter(models.Firm.owner_id == current_user.id).filter(models.Firm.fund_manager.contains(search)).limit(limit).offset(skip).all()
    # firms = db.query(models.Firm, func.count(models.Vote.firm_id).label("votes")).join(
    #     models.Vote, models.Vote.firm_id == models.Firm.code, isouter=True).group_by(models.Firm.code).filter(
    #     models.Firm.fund_manager.contains(search)).limit(limit).offset(skip).all()

    users = crud.get_users(db,
    skip=skip,
    limit=limit,
    min_last_changed_date=minimum_last_changed_date,
    firm_name=firm_name)

    return users
