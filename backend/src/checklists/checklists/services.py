from sqlalchemy.orm import Session
from auth import schemas as auth_schemas
from . import crud, models


async def create_checklist(checklist: models.Checklist, user: auth_schemas.TokenData, db: Session):
    return await crud.save_checklist(checklist, user.username, db)


async def get_checklist_by_id(checklist_id: int, user: auth_schemas.TokenData, db: Session):
    return await crud.get_checklist_by_id(checklist_id, user.username, db)


async def get_all_checklists(user: auth_schemas.TokenData, db: Session):
    return await crud.get_all_checklists(user.username, db)


async def delete_checklist(checklist_id: int, user: auth_schemas.TokenData, db: Session):
    return await crud.delete_checklist(checklist_id, user.username, db)
