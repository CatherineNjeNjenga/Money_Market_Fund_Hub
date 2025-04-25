from fastapi import Response, status, HTTPException, Depends, APIRouter, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from datetime import date
from .. import models, schemas, oauth2, crud
from ..database import get_db

router = APIRouter(
    prefix="/v0/counts",
    tags=['Analytics']
)

@router.get("/", response_model=schemas.Counts)
def get_count(db: Session = Depends(get_db)):
    counts = schemas.Counts(
        firm_count = crud.get_firm_count(db),
        user_count = crud.get_user_count(db),
        vote_count = crud.get_vote_count(db)
        )

    return counts