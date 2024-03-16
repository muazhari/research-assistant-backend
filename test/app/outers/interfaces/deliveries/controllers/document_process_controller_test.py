import json
from typing import List

import pytest as pytest
import pytest_asyncio
from test.utilities.test_client_utility import get_async_client

from app.inners.models.daos.account import Account
from app.inners.models.daos.document import Document
from app.inners.models.daos.document_process import DocumentProcess
from app.inners.models.daos.document_type import DocumentType
from app.inners.models.dtos.contracts.requests.managements.document_processes.create_one_body import CreateOneBody
from app.inners.models.dtos.contracts.requests.managements.document_processes.patch_one_body import PatchOneBody
from app.inners.models.dtos.contracts.result import Result
from app.outers.repositories.document_process_repository import DocumentProcessRepository
from test.app.outers.interfaces.deliveries.controllers.account_controller_test import account_repository
from test.app.outers.interfaces.deliveries.controllers.document_controller_test import document_repository
from test.app.outers.interfaces.deliveries.controllers.document_type_controller_test import document_type_repository
from test.mocks.document_process_mock import DocumentProcessMock

document_process_repository = DocumentProcessRepository()
document_process_mock_data = DocumentProcessMock()


@pytest_asyncio.fixture(scope="function", autouse=True)
async def run_around(request: pytest.FixtureRequest):
    for account in document_process_mock_data.document_mock_data.account_mock_data.data:
        await account_repository.create_one(Account(**account.dict()))
    for document_type in document_process_mock_data.document_mock_data.document_type_mock_data.data:
        await document_type_repository.create_one(DocumentType(**document_type.dict()))
    for document in document_process_mock_data.document_mock_data.data:
        await document_repository.create_one(Document(**document.dict()))
    for document_process in document_process_mock_data.data:
        await document_process_repository.create_one(DocumentProcess(**document_process.dict()))

    yield

    for document_process in document_process_mock_data.data:
        if request.node.name == "test__delete_one_by_id__should_delete_one_document_process__success" \
                and document_process.id == document_process_mock_data.data[0].id:
            continue
        await document_process_repository.delete_one_by_id(document_process.id)
    for document in document_process_mock_data.document_mock_data.data:
        await document_repository.delete_one_by_id(document.id)
    for document_type in document_process_mock_data.document_mock_data.document_type_mock_data.data:
        await document_type_repository.delete_one_by_id(document_type.id)
    for account in document_process_mock_data.document_mock_data.account_mock_data.data:
        await account_repository.delete_one_by_id(account.id)


@pytest.mark.asyncio
async def test__find_many__should_return_all_document_process__success():
    async with get_async_client() as client:
        response = await client.get(
            url="api/v1/document-processes"
        )
    assert response.status_code == 200
    result: Result[List[DocumentProcess]] = Result[List[DocumentProcess]](**response.json())
    assert all(document_process in content.data for document_process in document_process_mock_data.data)


@pytest.mark.asyncio
async def test__find_one_by_id__should_return_one_document_process__success():
    async with get_async_client() as client:
        response = await client.get(
            url=f"api/v1/document-processes/{document_process_mock_data.data[0].id}"
        )
        assert response.status_code == 200
        result: Result[DocumentProcess] = Result[DocumentProcess](**response.json())
        assert content.data == document_process_mock_data.data[0]


@pytest.mark.asyncio
async def test__create_one__should_create_one_document_process__success():
    body: CreateOneBody = CreateOneBody(
        initial_document_id=document_process_mock_data.document_mock_data.data[0].id,
        final_document_id=document_process_mock_data.document_mock_data.data[1].id,
        process_duration=2,
    )
    async with get_async_client() as client:
        response = await client.post(
            url="api/v1/document-processes",
            json=json.loads(body.json())
        )
        assert response.status_code == 200
        result: Result[DocumentProcess] = Result[DocumentProcess](**response.json())
        assert content.data.initial_document_id == body.initial_document_id
        assert content.data.final_document_id == body.final_document_id
        assert content.data.process_duration == body.process_duration
        document_process_mock_data.data.append(content.data)


@pytest.mark.asyncio
async def test__patch_one_by_id__should_patch_one_document_process__success():
    body: PatchOneBody = PatchOneBody(
        initial_document_id=document_process_mock_data.document_mock_data.data[1].id,
        final_document_id=document_process_mock_data.document_mock_data.data[0].id,
        process_duration=3,
    )
    async with get_async_client() as client:
        response = await client.patch(
            url=f"api/v1/document-processes/{document_process_mock_data.data[0].id}",
            json=json.loads(body.json())
        )
        assert response.status_code == 200
        result: Result[DocumentProcess] = Result[DocumentProcess](**response.json())
        assert content.data.initial_document_id == body.initial_document_id
        assert content.data.final_document_id == body.final_document_id
        assert content.data.process_duration == body.process_duration
        document_process_mock_data.data[0] = content.data


@pytest.mark.asyncio
async def test__delete_one_by_id__should_delete_one_document_process__success():
    async with get_async_client() as client:
        response = await client.delete(
            url=f"api/v1/document-processes/{document_process_mock_data.data[0].id}"
        )
        assert response.status_code == 200
        result: Result[DocumentProcess] = Result[DocumentProcess](**response.json())
        assert content.data == document_process_mock_data.data[0]
