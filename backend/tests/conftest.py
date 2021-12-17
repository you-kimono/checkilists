import pytest
from asgi_lifespan import LifespanManager
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.core import Base
from auth.api import get_db
from main import app

TEST_DATABASE_URL = 'sqlite:///./test.db'
test_engine = create_engine(
    TEST_DATABASE_URL, connect_args={'check_same_thread': False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


async def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope='function')
async def test_database():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope='function')
async def client() -> AsyncClient:
    app.dependency_overrides[get_db] = override_get_db
    async with LifespanManager(app):
        async with AsyncClient(
            app=app,
            base_url='http://testserver',
            headers={'Content-Type': 'application/json'}
        ) as client:
            Base.metadata.create_all(bind=test_engine)
            yield client
            Base.metadata.drop_all(bind=test_engine)
