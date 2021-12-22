from pydantic import BaseModel
from typing import List


class StepCreate(BaseModel):
    text: str
    description: str
    order: int


class Step(StepCreate):
    id: int
    is_completed: bool

    class Config:
        orm_mode = True


class ChecklistCreate(BaseModel):
    title: str
    description: str


class Checklist(ChecklistCreate):
    id: int
    steps: List[Step] = []

    class Config:
        orm_mode = True
