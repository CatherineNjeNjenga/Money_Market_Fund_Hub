from fastapi import Response, status, HTTPException, Depends, APIRouter, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from datetime import date
from .. import models, schemas, oauth2, crud
from ..database import get_db

router = APIRouter(
    prefix="/v0/reports",
    tags=['Rates']
)

@router.get("/", response_model=List[schemas.Report])
def read_reports(db: Session = Depends(get_db),
              skip: int = Query(0, description="The number of items to skip at the beginning of API call."), 
              limit: int = Query(10, description="The number of records to return after the skipped records."), 
              search: Optional[str] = "",
              minimum_last_changed_date: date =Query(None, description="The minimum date of change that you want to return records. Exclude any records changed before this.")):
    reports = crud.get_reports(db,
    skip=skip,
    limit=limit,
    min_last_changed_date=minimum_last_changed_date)

    return reports