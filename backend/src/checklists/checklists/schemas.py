from pydantic import BaseModel


class ChecklistCreate(BaseModel):
    title: str
    description: str
