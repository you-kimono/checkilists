from pydantic import BaseModel


class ChecklistCreate(BaseModel):
    title: str
    description: str


class Checklist(ChecklistCreate):
    id: int

    class Config:
        orm_mode = True


class StepCreate(BaseModel):
    text: str
    description: str
    order: int


class Step(StepCreate):
    id: int
    is_completed: bool

    class Config:
        orm_mode = True
