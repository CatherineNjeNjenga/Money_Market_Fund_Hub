from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter, Query
from typing import List, Optional
from datetime import date
from .. import schemas, database, models, oauth2
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(
  prefix="/vote",
  tags=['Votes']
)

@router.get("/", response_model=List[schemas.Vote]) # FirmOut
def read_votes(db: Session = Depends(get_db),
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

    votes = crud.get_votes(db,
    skip=skip,
    limit=limit,
    min_last_changed_date=minimum_last_changed_date,
    firm_name=firm_name)

    return votes


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user: int = Depends
         (oauth2.get_current_user)):
	
	post = db.query(models.Firm).filter(models.Post.id == vote.firm_id).first()
	if not post:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {vote.firm_id} does not exist")

	vote_query = db.query(models.Vote).filter(models.Vote.firm_id == vote.firm_id, models.Vote.user_id ==
		current_user.id)
	print(vote_query)
	found_vote = vote_query.first()
	if (vote.dir == 1):
		if found_vote:
			raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id} has already voted on post {vote.firm_id}")
		new_vote = models.Vote(firm_id = vote.firm_id, user_id = current_user.id)	
		db.add(new_vote)
		db.commit()
		return {"message": "successfully added vote"}
	else:
		if not found_vote:
			raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="vote does not exist")
		vote_query.delete(synchronize_session=False)
		db.commit()

		return {"message": "Successfully deleted vote"}
  