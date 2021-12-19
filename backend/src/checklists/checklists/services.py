from sqlalchemy.orm import Session
from . import crud, models


async def create_checklist(checklist: models.Checklist, db: Session):
    return await crud.save_checklist(checklist, db)


async def get_checklist_by_id(checklist_id: int, db: Session):
    return await crud.get_checklist_by_id(checklist_id, db)
