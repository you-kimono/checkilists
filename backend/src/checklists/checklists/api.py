from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database.core import engine, get_db
from auth import schemas as auth_schemas
from auth import oauth2
from . import exceptions, models, schemas, services


models.Base.metadata.create_all(bind=engine)
router = APIRouter()


@router.get('/', status_code=status.HTTP_200_OK)
async def get_all_checklists(
        db: Session = Depends(get_db),
        profile: auth_schemas.Profile = Depends(oauth2.get_current_user)
):
    return {'data': [
        'data1',
        'data2'
    ]}


@router.get('/{checklist_id}', status_code=status.HTTP_200_OK)
async def get_checklist(
        checklist_id: int,
        db: Session = Depends(get_db),
        profile: auth_schemas.Profile = Depends(oauth2.get_current_user)
):
    try:
        return await services.get_checklist_by_id(checklist_id, db)
    except exceptions.InvalidChecklist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'checklist with id {checklist_id} not found',
        )


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_checklist(
        request: schemas.ChecklistCreate,
        db: Session = Depends(get_db),
        profile: auth_schemas.Profile = Depends(oauth2.get_current_user)
):
    checklist = await services.create_checklist(models.Checklist(**request.dict()), db)
    return checklist
