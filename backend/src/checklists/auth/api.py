from fastapi import APIRouter
from database.core import SessionLocal
router = APIRouter()


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get('/')
def home():
    return {'prova': '0'}
