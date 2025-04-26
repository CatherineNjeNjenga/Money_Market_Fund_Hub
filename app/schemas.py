from pydantic import BaseModel, ConfigDict, EmailStr
from pydantic.types import conint
from typing import Optional, List
from datetime import datetime, date

class Report(BaseModel):
    model_config = ConfigDict(from_attributes = True)
    report_id: int
    firm_id: int
    week_number: str
    firm_rate: float
    last_changed_date: date


class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes = True)
    user_id: int
    email: EmailStr
    created_at: datetime
    last_changed_date: date

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Vote(BaseModel):
    firm_id: int
    dir: conint(le=1)

class FirmBase(BaseModel):
    model_config = ConfigDict(from_attributes = True)
    firm_id: int
    firm_name: str
    licenced: bool
    last_changed_date: date

class Firm(FirmBase):
    model_config = ConfigDict(from_attributes = True)
    reports: List[Report] = []
    votes: List[Vote] = []
    

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None


class Counts(BaseModel):
    firm_count: int
    user_count: int
    vote_count: int

# class FirmOut(BaseModel):
#     model_config = ConfigDict(from_attributes = True)
#     Firm: Firm
#     votes: int
