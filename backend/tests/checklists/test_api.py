import pytest

from fastapi import status
from httpx import AsyncClient

from checklists import schemas


@pytest.fixture
def new_checklist():
    return schemas.ChecklistCreate(
        title="checklist title",
        description="checklist description"
    )


class TestUnauthenticatedRoutes:

    @pytest.mark.asyncio
    async def test_get_all_checklists(
            self,
            client: AsyncClient
    ) -> None:
        response = await client.get('/checklists/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.asyncio
    async def test_get_checklist(
            self,
            client: AsyncClient
    ) -> None:
        response = await client.get('/checklists/1')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.asyncio
    async def test_create_checklist(
            self,
            client: AsyncClient,
            new_checklist: schemas.ChecklistCreate
    ) -> None:
        response = await client.post('/checklists/', json=new_checklist.dict())
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestAuthenticatedRoutes:

    @pytest.mark.asyncio
    async def test_get_all_checklists(
            self,
            authorized_client: AsyncClient
    ) -> None:

        response = await authorized_client.get('/checklists/')
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.asyncio
    async def test_get_checklist(
            self,
            authorized_client: AsyncClient
    ) -> None:
        response = await authorized_client.get('/checklists/1')
        assert response.status_code != status.HTTP_401_UNAUTHORIZED

    @pytest.mark.asyncio
    async def test_create_checklist(
            self,
            authorized_client: AsyncClient,
            new_checklist: schemas.ChecklistCreate
    ) -> None:
        response = await authorized_client.post('/checklists/', json=new_checklist.dict())
        assert response.status_code == status.HTTP_201_CREATED


class TestPostRoute:

    @pytest.mark.asyncio
    async def test_invalid_input_raises_error(
            self,
            authorized_client: AsyncClient
    ) -> None:
        response = await authorized_client.post('/checklists/', json={})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    @pytest.mark.asyncio
    async def test_create_checklist(
            self,
            authorized_client: AsyncClient,
            new_checklist: schemas.ChecklistCreate
    ) -> None:
        response = await authorized_client.post('/checklists/', json=new_checklist.dict())
        assert response.status_code == status.HTTP_201_CREATED

        data = response.json()
        assert 'id' in data
        checklist_id: int = data['id']

        response = await authorized_client.get(f'/checklists/{checklist_id}')
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data['title'] == new_checklist.title
        assert data['description'] == new_checklist.description


class TestGetChecklist:

    @pytest.mark.asyncio
    async def test_get_non_existing_checklist_raises_exception(
            self,
            authorized_client: AsyncClient
    ) -> None:
        checklist_id: int = 666
        response = await authorized_client.get(f'/checklists/{checklist_id}')
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()['detail'] == f'checklist with id {checklist_id} not found'
