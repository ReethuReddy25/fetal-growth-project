from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: str
    class Config:
        orm_mode = True

class LoginIn(BaseModel):
    email: EmailStr
    password: str

class PredictIn(BaseModel):
    ga_weeks: float
    # files are sent via multipart/form-data; not here
