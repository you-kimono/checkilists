import pytest

from fastapi import status
from httpx import AsyncClient
from auth import schemas


@pytest.fixture
def new_profile():
    return schemas.ProfileCreate(
        email="test@test.com",
        password="test_password"
    )


@pytest.fixture
def another_new_profile():
    return schemas.ProfileCreate(
        email="another@test.com",
        password="another_password"
    )


class TestRegister:

    @pytest.mark.asyncio
    async def test_post_route_exists(
            self,
            client: AsyncClient
    ) -> None:
        response = await client.post('/register', json={})
        assert response.status_code != status.HTTP_404_NOT_FOUND
        assert response.status_code != status.HTTP_405_METHOD_NOT_ALLOWED
        assert response.status_code != status.HTTP_307_TEMPORARY_REDIRECT

    @pytest.mark.asyncio
    async def test_post_invalid_input_raises_error(
            self,
            client: AsyncClient
    ) -> None:
        response = await client.post('/register', json={})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    @pytest.mark.asyncio
    async def test_post_valid_input_returns_expected_code(
            self,
            client: AsyncClient,
            new_profile: schemas.ProfileCreate
    ) -> None:
        response = await client.post('/register', json=new_profile.dict())
        assert response.status_code == status.HTTP_201_CREATED

    @pytest.mark.asyncio
    async def test_post_email_must_be_unique(
            self,
            client: AsyncClient,
            new_profile: schemas.ProfileCreate
    ) -> None:
        await client.post('/register', json={
            "email": "test@test.com",
            "password": "test_password"
        })
        response = await client.post('/register', json={
            "email": "test@test.com",
            "password": "another_password"
        })
        assert response.status_code == status.HTTP_409_CONFLICT

    @pytest.mark.asyncio
    async def test_post_password_must_not_be_unique(
            self,
            client: AsyncClient,
            new_profile: schemas.ProfileCreate
    ) -> None:
        await client.post('/register', json={
            "email": "test@test.com",
            "password": "test_password"
        })
        response = await client.post('/register', json={
            "email": "another@test.com",
            "password": "test_password"
        })
        assert response.status_code == status.HTTP_201_CREATED

    @pytest.mark.asyncio
    async def test_create_profile_as_expected_data(
            self,
            client: AsyncClient,
            new_profile: schemas.ProfileCreate
    ) -> None:
        response = await client.post('/register', json=new_profile.dict())
        data = response.json()
        assert data['email'] == new_profile.email
        assert 'id' in data
        profile_id: int = data['id']

        response = await client.get(f'/profiles/{profile_id}')
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data['email'] == new_profile.email
        assert data['id'] == profile_id


class TestLogin:

    @pytest.mark.asyncio
    async def test_login_with_valid_credentials(
            self,
            client: AsyncClient,
            new_profile: schemas.ProfileCreate
    ) -> None:
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
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert '' != data['access_token']
        assert 'bearer' == data['token_type']


class TestDeleteProfile:

    @pytest.mark.asyncio
    async def test_delete_existing_profile(
            self,
            client: AsyncClient,
            new_profile: schemas.ProfileCreate
    ) -> None:
        await client.post('/register', json=new_profile.dict())
        response = await client.delete(f'/profiles/1')
        assert response.status_code == status.HTTP_202_ACCEPTED
        response = await client.get(f'/profiles/1')
        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.asyncio
    async def test_delete_non_existing_profile(
            self,
            client: AsyncClient
    ) -> None:
        response = await client.delete(f'/profiles/1')
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()['detail'] == 'profile with id 1 not found'
