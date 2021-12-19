import pytest
from asgi_lifespan import LifespanManager
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from auth import schemas
from database.core import Base, get_db
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


@pytest.fixture(scope='function')
async def authorized_client(client: AsyncClient):
    new_profile: schemas.ProfileCreate = schemas.ProfileCreate(
        email="test@test.com",
        password="test_password"
    )
    await client.post('/register', json=new_profile.dict())
    response = await client.post(
        '/login',
        data={
            'username': new_profile.email,
            'password': new_profile.password
        },
        headers={
            "Content-Type": "application/x-www-form-urlencoded"
        },
    )
    access_token = response.json()['access_token']
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {access_token}",
    }
    yield client
