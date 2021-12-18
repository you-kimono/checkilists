from pydantic import BaseModel
from pydantic import EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class User(UserCreate):
    id: int

    class Config:
        orm_mode = True


class ShowUser(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True
