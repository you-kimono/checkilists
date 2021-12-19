from pydantic import BaseModel
from pydantic import EmailStr
from typing import Optional


class ProfileCreate(BaseModel):
    email: EmailStr
    password: str


class Profile(ProfileCreate):
    id: int

    class Config:
        orm_mode = True


class ShowProfile(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True


class Login(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
