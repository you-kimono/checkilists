from pydantic import BaseModel


class ChecklistCreate(BaseModel):
    title: str
    description: str


class Checklist(ChecklistCreate):
    id: int

    class Config:
        orm_mode = True
