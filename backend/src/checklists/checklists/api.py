from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database.core import engine, get_db
from auth import models, schemas
from auth import oauth2


models.Base.metadata.create_all(bind=engine)
router = APIRouter()


@router.get('/', status_code=status.HTTP_200_OK)
async def get_all_checklists(
        db: Session = Depends(get_db),
        profile: schemas.Profile = Depends(oauth2.get_current_user)
):
    return {'data': [
        'data1',
        'data2'
    ]}
