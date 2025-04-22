from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/firms",
    tags=['Firms']
)

@router.get("/", response_model=List[schemas.FirmOut])
def get_firms(db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user),
              limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # sqlite
    # cursor.execute("""SELECT * FROM firms""")
    # firms = cursor.fetchall()

    # sqlalchemy
    # firms = db.query(models.Firm).filter(models.Firm.owner_id == current_user.id).filter(models.Firm.fund_manager.contains(search)).limit(limit).offset(skip).all()
    firms = db.query(models.Firm, func.count(models.Vote.firm_id).label("votes")).join(
        models.Vote, models.Vote.firm_id == models.Firm.code, isouter=True).group_by(models.Firm.code).filter(
        models.Firm.fund_manager.contains(search)).limit(limit).offset(skip).all()

    return firms

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Firm)
def create_firms(firm: schemas.FirmCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # sqlite
    # cursor.execute("""INSERT INTO firms (code, fund_manager) VALUES (:code, :fund_manager) RETURNING * """, 
    #               {'code':firm.code, 'fund_manager':firm.fund_manager})
    # new_firm = cursor.fetchone()
    # conn.commit()
    # **firm.dict()

    # sqlalchemy
    new_firm = models.Firm(owner_id=current_user.id, **firm.model_dump())
    
    db.add(new_firm)
    db.commit()
    db.refresh(new_firm)
    return new_firm

@router.get("/{code}", response_model=schemas.FirmOut)
def get_firm(code: int, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    # sqlite
    # cursor.execute("""SELECT * FROM firms WHERE code = ? """, [str(code)])
    # firm = cursor.fetchone()

    # sqlalchemy
    # firm = db.query(models.Firm).filter(models.Firm.code == code).first()
    firm = db.query(models.Firm, func.count(models.Vote.firm_id).label("votes")).join(
        models.Vote, models.Vote.firm_id == models.Firm.code, isouter=True).group_by(models.Firm.code).filter(
        models.Firm.code == code).first()
    print(firm)
    if not firm:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"firm with code: {code} not found")
   
    return firm

@router.delete("/{code}", status_code=status.HTTP_204_NO_CONTENT)
def delete_firm(code: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # sqlite
    # cursor.execute("""DELETE FROM firms WHERE code = ? RETURNING *""", [str(code)])
    # deleted_firm = cursor.fetchone()
    # conn.commit()

    # sqlalchemy
    firm_query = db.query(models.Firm).filter(models.Firm.code == code)
    firm = firm_query.first()
    if not firm:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"firm with code: {code} not found")
    if firm.owner_id != current_user.id:
        raise  HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action.")
    firm_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{code}", response_model=schemas.Firm)
def update_firm(code: int, firm: schemas.FirmCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # sqlite
    # cursor.execute("""UPDATE firms SET code = ? ,fund_manager = ? WHERE code = ? RETURNING *""", (firm.code, firm.fund_manager, str(code)))
    # updated_firm = cursor.fetchone()
    # conn.commit()

    # sqlalchemy
    updated_firm = db.query(models.Firm).filter(models.Firm.code == code)

    if not updated_firm.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"firm with code: {code} not found")
    if firm.owner_id != current_user.id:
        raise  HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action.")
    updated_firm.update(firm.model_dump(), synchronize_session=False)
    db.commit()

    return updated_firm.first()
