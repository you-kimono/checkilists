import pytest

from fastapi import status
from httpx import AsyncClient
from auth import schemas


@pytest.fixture
def new_user():
    return schemas.UserCreate(
        email="test@test.com",
        password="test_password"
    )


@pytest.fixture
def another_new_user():
    return schemas.UserCreate(
        email="another@test.com",
        password="another_password"
    )


class TestPostUser:

    @pytest.mark.asyncio
    async def test_post_route_exists(
            self,
            client: AsyncClient
    ) -> None:
        response = await client.post('/users/', json={})
        assert response.status_code != status.HTTP_404_NOT_FOUND
        assert response.status_code != status.HTTP_405_METHOD_NOT_ALLOWED
        assert response.status_code != status.HTTP_307_TEMPORARY_REDIRECT

    @pytest.mark.asyncio
    async def test_post_invalid_input_raises_error(
            self,
            client: AsyncClient
    ) -> None:
        response = await client.post('/users/', json={})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    @pytest.mark.asyncio
    async def test_post_valid_input_returns_expected_code(
            self,
            client: AsyncClient,
            new_user: schemas.UserCreate
    ) -> None:
        response = await client.post('/users/', json=new_user.dict())
        assert response.status_code == status.HTTP_201_CREATED

    @pytest.mark.asyncio
    async def test_post_email_must_be_unique(
            self,
            client: AsyncClient,
            new_user: schemas.UserCreate
    ) -> None:
        await client.post('/users/', json={
            "email": "test@test.com",
            "password": "test_password"
        })
        response = await client.post('/users/', json={
            "email": "test@test.com",
            "password": "another_password"
        })
        assert response.status_code == status.HTTP_409_CONFLICT

    @pytest.mark.asyncio
    async def test_post_password_must_not_be_unique(
            self,
            client: AsyncClient,
            new_user: schemas.UserCreate
    ) -> None:
        await client.post('/users/', json={
            "email": "test@test.com",
            "password": "test_password"
        })
        response = await client.post('/users/', json={
            "email": "another@test.com",
            "password": "test_password"
        })
        assert response.status_code == status.HTTP_201_CREATED


class TestCreateUser:

    @pytest.mark.asyncio
    async def test_create_user(
            self,
            client: AsyncClient,
            new_user: schemas.UserCreate
    ) -> None:
        response = await client.post('/users/', json=new_user.dict())
        data = response.json()
        assert data['email'] == new_user.email
        assert 'id' in data
        user_id: int = data['id']

        response = await client.get(f'/users/{user_id}')
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data['email'] == new_user.email
        assert data['id'] == user_id

    @pytest.mark.asyncio
    async def test_created_user_has_the_same_email(
            self,
            client: AsyncClient,
            new_user: schemas.UserCreate
    ) -> None:
        response = await client.post('/users/', json=new_user.dict())
        data = response.json()
        user_id: int = data['id']

        response = await client.get(f'/users/{user_id}')
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data['email'] == new_user.email


class TestDeleteUser:

    @pytest.mark.asyncio
    async def test_delete_existing_user(
            self,
            client: AsyncClient,
            new_user: schemas.UserCreate
    ) -> None:
        await client.post('/users/', json=new_user.dict())
        response = await client.delete(f'/users/1')
        assert response.status_code == status.HTTP_202_ACCEPTED
        response = await client.get(f'/users/1')
        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.asyncio
    async def test_delete_non_existing_user(
            self,
            client: AsyncClient,
            new_user: schemas.UserCreate
    ) -> None:
        response = await client.delete(f'/users/1')
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()['detail'] == 'user with id 1 not found'
