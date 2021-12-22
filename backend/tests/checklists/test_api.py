import pytest

from fastapi import status
from httpx import AsyncClient

from checklists import schemas


@pytest.fixture
def new_checklist() -> schemas.ChecklistCreate:
    return schemas.ChecklistCreate(
        title="checklist title",
        description="checklist description"
    )


@pytest.fixture
def new_simple_step() -> schemas.StepCreate:
    return schemas.StepCreate(
        text="step 1",
        description="perform step 1",
        order=0
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

    @pytest.mark.asyncio
    async def test_delete_checklist(
            self,
            client: AsyncClient
    ) -> None:
        response = await client.delete('/checklists/1')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.asyncio
    async def test_get_step(
            self,
            client: AsyncClient,
            new_checklist: schemas.ChecklistCreate
    ) -> None:
        await client.post('/checklists/', json=new_checklist.dict())
        response = await client.get('/checklists/1/steps/1')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.asyncio
    async def test_create_step(
            self,
            client: AsyncClient,
            new_checklist: schemas.ChecklistCreate
    ) -> None:
        response = await client.post('/checklists/1/steps', json=new_checklist.dict())
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.asyncio
    async def test_delete_step(
            self,
            client: AsyncClient
    ) -> None:
        response = await client.delete('/checklists/1/steps/1')
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

    @pytest.mark.asyncio
    async def test_create_checklist(
            self,
            authorized_client: AsyncClient,
            new_checklist: schemas.ChecklistCreate
    ) -> None:
        await authorized_client.post('/checklists/', json=new_checklist.dict())
        response = await authorized_client.delete('/checklists/1')
        assert response.status_code == status.HTTP_202_ACCEPTED

    @pytest.mark.asyncio
    async def test_create_step(
            self,
            authorized_client: AsyncClient,
            new_checklist: schemas.ChecklistCreate,
            new_simple_step: schemas.StepCreate
    ) -> None:
        await authorized_client.post('/checklists/', json=new_checklist.dict())
        response = await authorized_client.post('/checklists/1/steps', json=new_simple_step.dict())
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


class TestGetChecklists:

    @pytest.mark.asyncio
    async def test_get_all_checklists_returns_expected_results(
            self,
            authorized_client: AsyncClient,
            new_checklist: schemas.ChecklistCreate
    ) -> None:
        response = await authorized_client.post('/checklists/', json=new_checklist.dict())
        checklist_1 = schemas.Checklist(**response.json())
        response = await authorized_client.post('/checklists/', json=new_checklist.dict())
        checklist_2 = schemas.Checklist(**response.json())

        response = await authorized_client.get(f'/checklists/')
        assert response.status_code == status.HTTP_200_OK
        assert checklist_1 in response.json()
        assert checklist_2 in response.json()


class TestDeleteChecklist:

    @pytest.mark.asyncio
    async def test_delete_existing_checklist(
            self,
            authorized_client: AsyncClient,
            new_checklist: schemas.ChecklistCreate
    ) -> None:
        await authorized_client.post('/checklists/', json=new_checklist.dict())
        response = await authorized_client.delete(f'/checklists/1')
        assert response.status_code == status.HTTP_202_ACCEPTED
        response = await authorized_client.get(f'/checklists/1')
        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.asyncio
    async def test_delete_non_existing_checklist(
            self,
            authorized_client: AsyncClient
    ) -> None:
        response = await authorized_client.delete(f'/checklists/1')
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()['detail'] == 'checklist with id 1 not found'


class TestPostStepRoute:

    @pytest.mark.asyncio
    async def test_invalid_input_raises_error(
            self,
            authorized_client: AsyncClient,
            new_checklist: schemas.ChecklistCreate
    ) -> None:
        await authorized_client.post('/checklists/', json=new_checklist.dict())
        response = await authorized_client.post('/checklists/1/steps', json={})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    @pytest.mark.asyncio
    async def test_create_step(
            self,
            authorized_client: AsyncClient,
            new_checklist: schemas.ChecklistCreate,
            new_simple_step: schemas.StepCreate
    ) -> None:
        response = await authorized_client.post('/checklists/', json=new_checklist.dict())
        checklist_id: int = response.json()['id']

        response = await authorized_client.post(f'/checklists/{checklist_id}/steps', json=new_simple_step.dict())

        assert response.status_code == status.HTTP_201_CREATED

        data = response.json()
        assert 'id' in data
        step_id: int = data['id']

        response = await authorized_client.get(f'/checklists/{checklist_id}/steps/{step_id}')
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data['text'] == new_simple_step.text
        assert data['description'] == new_simple_step.description
        assert data['order'] == new_simple_step.order
        assert not data['is_completed']


class TestGetStep:

    @pytest.mark.asyncio
    async def test_get_non_existing_step_raises_exception(
            self,
            authorized_client: AsyncClient,
            new_checklist: schemas.ChecklistCreate
    ) -> None:
        response = await authorized_client.post('/checklists/', json=new_checklist.dict())
        checklist_id: int = response.json()['id']

        step_id: int = 666
        response = await authorized_client.get(f'/checklists/{checklist_id}/steps/{step_id}')
        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.asyncio
    async def test_get_step_of_non_existing_checklist_raises_exception(
            self,
            authorized_client: AsyncClient,
            new_checklist: schemas.ChecklistCreate,
            new_simple_step: schemas.StepCreate
    ) -> None:
        response = await authorized_client.post('/checklists/', json=new_checklist.dict())
        checklist_id: int = response.json()['id']

        response = await authorized_client.post(f'/checklists/{checklist_id}/steps', json=new_simple_step.dict())
        step_id: int = response.json()['id']

        missing_checklist_id: int = 666
        response = await authorized_client.get(f'/checklists/{missing_checklist_id}/steps/{step_id}')
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestDeleteStep:

    @pytest.mark.asyncio
    async def test_delete_existing_step(
            self,
            authorized_client: AsyncClient,
            new_checklist: schemas.ChecklistCreate,
            new_simple_step: schemas.StepCreate
    ) -> None:
        response = await authorized_client.post('/checklists/', json=new_checklist.dict())
        checklist_id: int = response.json()['id']

        response = await authorized_client.post(f'/checklists/{checklist_id}/steps', json=new_simple_step.dict())
        step_id: int = response.json()['id']

        response = await authorized_client.delete(f'/checklists/{checklist_id}/steps/{step_id}')
        assert response.status_code == status.HTTP_202_ACCEPTED
        response = await authorized_client.get(f'/checklists/{checklist_id}/steps/{step_id}')
        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.asyncio
    async def test_delete_non_existing_step(
            self,
            authorized_client: AsyncClient,
            new_checklist: schemas.ChecklistCreate
    ) -> None:
        response = await authorized_client.post('/checklists/', json=new_checklist.dict())
        checklist_id: int = response.json()['id']

        response = await authorized_client.delete(f'/checklists/{checklist_id}/steps/1')
        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.asyncio
    async def test_delete_step_of_non_existing_checklist(
            self,
            authorized_client: AsyncClient,
            new_checklist: schemas.ChecklistCreate,
            new_simple_step: schemas.StepCreate
    ) -> None:
        response = await authorized_client.post('/checklists/', json=new_checklist.dict())
        checklist_id: int = response.json()['id']

        response = await authorized_client.post(f'/checklists/{checklist_id}/steps', json=new_simple_step.dict())
        step_id: int = response.json()['id']

        missing_checklist_id: int = 666
        response = await authorized_client.delete(f'/checklists/{missing_checklist_id}/steps/{step_id}')
        assert response.status_code == status.HTTP_404_NOT_FOUND
