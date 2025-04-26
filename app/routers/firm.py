from fastapi import Response, status, HTTPException, Depends, APIRouter, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from datetime import date
from .. import models, schemas, oauth2, crud
from ..database import get_db

router = APIRouter(
    prefix="/v0/firms",
    tags=['Firms']
)

@router.get("/", response_model=List[schemas.Firm])
def read_firms(db: Session = Depends(get_db),
              skip: int = Query(0, description="The number of items to skip at the beginning of API call."), 
              limit: int = Query(10, description="The number of records to return after the skipped records."),
              search: Optional[str] = "",
              minimum_last_changed_date: date = Query(None, description="The minimum date of change that you want to return records. Exclude any records changed before this."), 
              firm_name: str = Query(None, description="The name of the firms to return")
              #current_user: int = Depends(oauth2.get_current_user),
              ):
    firms = crud.get_firms(
        db,
        skip=skip,
        limit=limit,
        min_last_changed_date=minimum_last_changed_date,
        firm_name=firm_name)

    return firms

@router.get("/{firm_id}", response_model=schemas.Firm,
            summary="Get one firm using the Firm ID, which is internal to MMFH",
            description="If you have an MMFH Firm ID of a firm from another API call such as v0_get_firms, you can call this API using the firm ID",
            response_description="One Fund Manager firm",
            operation_id="v0_get_firms_by_firm_id")
def read_firm(firm_id: int, db: Session = Depends(get_db),
              #current_user: int = Depends(oauth2.get_current_user)
            ):
    firm = crud.get_firm(db, firm_id = firm_id)
    if not firm:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"firm with id: {firm_id} not found")
   
    return firm

