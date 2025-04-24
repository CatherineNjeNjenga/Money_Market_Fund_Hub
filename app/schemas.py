from pydantic import BaseModel,EmailStr
from pydantic.types import conint
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class FirmBase(BaseModel):
    code: int
    fund_manager: str
    week_1: str
    week_2: str
    week_3: str
    week_4: str
    week_5: str
    week_6: str
    week_7: str
    week_8: str

class FirmCreate(FirmBase):
    pass

class Firm(FirmBase):
    owner_id: int
    owner: UserOut
    created_at: datetime

    class Config:
        from_attributes = True

class FirmOut(BaseModel):
    Firm: Firm
    votes: int

    class Config:
        from_attributes = True

class FirmsOut(BaseModel):
    Firm: Firm
    votes: int

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None

class Vote(BaseModel):
    firm_id: int
    dir: conint(le=1)
