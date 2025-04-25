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

@router.get("/", response_model=List[schemas.Firm]) # FirmOut
def read_firms(db: Session = Depends(get_db),
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

    firms = crud.get_firms(db,
    skip=skip,
    limit=limit,
    min_last_changed_date=minimum_last_changed_date,
    firm_name=firm_name)

    return firms

@router.get("/{firm_id}", response_model=schemas.Firm,
summary="Get one firm using the Firm ID, which is internal to MMFH",
description="If you have an MMFH Firm ID of a firm from another API call such as v0_get_firms, you can call this API using the firm ID",
response_description="One Fund Manager firm",
operation_id="v0_get_firms_by_firm_id") # FirmOut
def read_firm(firm_id: int, db: Session = Depends(get_db),
#current_user: int = Depends(oauth2.get_current_user)
):
    # sqlite
    # cursor.execute("""SELECT * FROM firms WHERE code = ? """, [str(code)])
    # firm = cursor.fetchone()

    # sqlalchemy
    # firm = db.query(models.Firm).filter(models.Firm.code == code).first()
    # firm = db.query(models.Firm, func.count(models.Vote.firm_id).label("votes")).join(
    #     models.Vote, models.Vote.firm_id == models.Firm.code, isouter=True).group_by(models.Firm.code).filter(
    #     models.Firm.code == code).first()
    # print(firm)
    firm = crud.get_firm(db, firm_id = firm_id)
    if not firm:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"firm with id: {firm_id} not found")
   
    return firm

# @router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Firm)
# def create_firms(firm: schemas.FirmCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
#     # sqlite
#     # cursor.execute("""INSERT INTO firms (code, fund_manager) VALUES (:code, :fund_manager) RETURNING * """, 
#     #               {'code':firm.code, 'fund_manager':firm.fund_manager})
#     # new_firm = cursor.fetchone()
#     # conn.commit()
#     # **firm.dict()

#     # sqlalchemy
#     new_firm = models.Firm(owner_id=current_user.id, **firm.model_dump())
    
#     db.add(new_firm)
#     db.commit()
#     db.refresh(new_firm)
#     return new_firm

# @router.delete("/{code}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_firm(code: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
#     # sqlite
#     # cursor.execute("""DELETE FROM firms WHERE code = ? RETURNING *""", [str(code)])
#     # deleted_firm = cursor.fetchone()
#     # conn.commit()

#     # sqlalchemy
#     firm_query = db.query(models.Firm).filter(models.Firm.code == code)
#     firm = firm_query.first()
#     if not firm:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"firm with code: {code} not found")
#     if firm.owner_id != current_user.id:
#         raise  HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action.")
#     firm_query.delete(synchronize_session=False)
#     db.commit()

#     return Response(status_code=status.HTTP_204_NO_CONTENT)

# @router.put("/{code}", response_model=schemas.Firm)
# def update_firm(code: int, firm: schemas.FirmCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
#     # sqlite
#     # cursor.execute("""UPDATE firms SET code = ? ,fund_manager = ? WHERE code = ? RETURNING *""", (firm.code, firm.fund_manager, str(code)))
#     # updated_firm = cursor.fetchone()
#     # conn.commit()

#     # sqlalchemy
#     updated_firm = db.query(models.Firm).filter(models.Firm.code == code)

#     if not updated_firm.first():
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"firm with code: {code} not found")
#     if firm.owner_id != current_user.id:
#         raise  HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action.")
#     updated_firm.update(firm.model_dump(), synchronize_session=False)
#     db.commit()

#     return updated_firm.first()
