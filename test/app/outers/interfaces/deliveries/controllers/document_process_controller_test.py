import json
from typing import List

import pytest as pytest
import pytest_asyncio

from app.inners.models.entities.account import Account
from app.inners.models.entities.document import Document
from app.inners.models.entities.document_process import DocumentProcess
from app.inners.models.entities.document_type import DocumentType
from app.inners.models.value_objects.contracts.requests.managements.document_processes.create_body import CreateBody
from app.inners.models.value_objects.contracts.requests.managements.document_processes.patch_body import PatchBody
from app.inners.models.value_objects.contracts.responses.content import Content
from app.outers.repositories.document_process_repository import DocumentProcessRepository
from test.app.outers.interfaces.deliveries.controllers.account_controller_test import account_repository
from test.app.outers.interfaces.deliveries.controllers.document_controller_test import document_repository
from test.app.outers.interfaces.deliveries.controllers.document_type_controller_test import document_type_repository
from test.mock_data.document_process_mock_data import DocumentProcessMockData
from test.utilities.test_client_utility import get_async_client

test_client = get_async_client()
document_process_repository = DocumentProcessRepository()
document_process_mock_data = DocumentProcessMockData()


@pytest_asyncio.fixture(scope="function", autouse=True)
async def run_around(request: pytest.FixtureRequest):
    for account in document_process_mock_data.document_mock_data.data:
        await account_repository.create_one(Account(**account.dict()))
    for document_type in document_process_mock_data.document_mock_data.data:
        await document_type_repository.create_one(DocumentType(**document_type.dict()))
    for document in document_process_mock_data.document_mock_data:
        await document_repository.create_one(Document(**document.dict()))
    for document_process in document_process_mock_data.data:
        await document_process_repository.create_one(DocumentProcess(**document_process.dict()))

    yield

    for document_process in document_process_mock_data.data:
        if request.node.name == "test__delete_one_by_id__should_delete_one_document_process__success" \
                and document_process.id == document_process_mock_data.data[0].id:
            continue
        await document_process_repository.delete_one_by_id(document_process.id)
    for document in document_process_mock_data.document_mock_data:
        await document_repository.delete_one_by_id(document.id)
    for document_type in document_process_mock_data.document_mock_data.data:
        await document_type_repository.delete_one_by_id(document_type.id)
    for account in document_process_mock_data.document_mock_data.data:
        await account_repository.delete_one_by_id(account.id)


@pytest.mark.asyncio
async def test__read_all__should_return_all_document_processs__success():
    response = await test_client.get(
        url="api/v1/document-processes"
    )
    assert response.status_code == 200
    content: Content[List[DocumentProcess]] = Content[List[DocumentProcess]](**response.json())
    assert all(document_process in content.data for document_process in document_process_mock_data.data)


@pytest.mark.asyncio
async def test__read_one_by_id__should_return_one_document_process__success():
    response = await test_client.get(
        url=f"api/v1/document-processes/{document_process_mock_data.data[0].id}"
    )
    assert response.status_code == 200
    content: Content[DocumentProcess] = Content[DocumentProcess](**response.json())
    assert content.data == document_process_mock_data.data[0]


@pytest.mark.asyncio
async def test__create_one__should_create_one_document_process__success():
    document_process_create: CreateBody = CreateBody(
        initial_document_id=document_process_mock_data.document_mock_data[0].id,
        final_document_id=document_process_mock_data.document_mock_data[1].id,
        process_duration=2,
    )
    response = await test_client.post(
        url="api/v1/document-processes",
        json=json.loads(document_process_create.json())
    )
    assert response.status_code == 200
    content: Content[DocumentProcess] = Content[DocumentProcess](**response.json())
    assert content.data.initial_document_id == document_process_create.initial_document_id
    assert content.data.final_document_id == document_process_create.final_document_id
    assert content.data.process_duration == document_process_create.process_duration
    document_process_mock_data.data.append(content.data)


@pytest.mark.asyncio
async def test__patch_one_by_id__should_patch_one_document_process__success():
    document_process_patch: PatchBody = PatchBody(
        initial_document_id=document_process_mock_data.document_mock_data[1].id,
        final_document_id=document_process_mock_data.document_mock_data[0].id,
        process_duration=3,
    )
    response = await test_client.patch(
        url=f"api/v1/document-processes/{document_process_mock_data.data[0].id}",
        json=json.loads(document_process_patch.json())
    )
    assert response.status_code == 200
    content: Content[DocumentProcess] = Content[DocumentProcess](**response.json())
    assert content.data.initial_document_id == document_process_patch.initial_document_id
    assert content.data.final_document_id == document_process_patch.final_document_id
    assert content.data.process_duration == document_process_patch.process_duration
    document_process_mock_data.data[0] = content.data


@pytest.mark.asyncio
async def test__delete_one_by_id__should_delete_one_document_process__success():
    response = await test_client.delete(
        url=f"api/v1/document-processes/{document_process_mock_data.data[0].id}"
    )
    assert response.status_code == 200
    content: Content[DocumentProcess] = Content[DocumentProcess](**response.json())
    assert content.data == document_process_mock_data.data[0]
