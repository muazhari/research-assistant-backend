import json
from typing import List

import pytest as pytest
import pytest_asyncio
from test.utilities.test_client_utility import get_async_client

from app.inners.models.daos.account import Account
from app.inners.models.daos.document import Document
from app.inners.models.daos.document_type import DocumentType
from app.inners.models.dtos.contracts.requests.managements.documents.create_one_body import \
    CreateOneBody
from app.inners.models.dtos.contracts.requests.managements.documents.patch_one_body import \
    PatchOneBody
from app.inners.models.dtos.contracts.result import Result
from app.outers.repositories.document_repository import DocumentRepository
from test.app.outers.interfaces.deliveries.controllers.account_controller_test import account_repository
from test.app.outers.interfaces.deliveries.controllers.document_type_controller_test import document_type_repository
from test.mocks.document_mock import DocumentMock

document_repository = DocumentRepository()
document_mock_data = DocumentMock()


@pytest_asyncio.fixture(scope="function", autouse=True)
async def run_around(request: pytest.FixtureRequest):
    for account in document_mock_data.account_mock_data.data:
        await account_repository.create_one(Account(**account.dict()))
    for document_type in document_mock_data.document_type_mock_data.data:
        await document_type_repository.create_one(DocumentType(**document_type.dict()))
    for document in document_mock_data.data:
        await document_repository.create_one(Document(**document.dict()))

    yield

    for document in document_mock_data.data:
        if request.node.name == "test__delete_one_by_id__should_delete_one_document__success" \
                and document.id == document_mock_data.data[0].id:
            continue
        await document_repository.delete_one_by_id(document.id)
    for document_type in document_mock_data.document_type_mock_data.data:
        await document_type_repository.delete_one_by_id(document_type.id)
    for account in document_mock_data.account_mock_data.data:
        await account_repository.delete_one_by_id(account.id)


@pytest.mark.asyncio
async def test__find_many__should_return_all_documents__success():
    async with get_async_client() as client:
        response = await client.get(
            url="api/v1/documents"
        )
        assert response.status_code == 200
        result: Result[List[Document]] = Result[List[Document]](**response.json())
        assert all(document in content.data for document in document_mock_data.data)


@pytest.mark.asyncio
async def test__find_one_by_id__should_return_one_document__success():
    async with get_async_client() as client:
        response = await client.get(
            url=f"api/v1/documents/{document_mock_data.data[0].id}"
        )
        assert response.status_code == 200
        result: Result[Document] = Result[Document](**response.json())
        assert content.data == document_mock_data.data[0]


@pytest.mark.asyncio
async def test__create_one__should_create_one_document__success():
    body: CreateOneBody = CreateOneBody(
        name="name2",
        description="description2",
        account_id=document_mock_data.account_mock_data.data[0].id,
        document_type_id=document_mock_data.document_type_mock_data.data[0].id
    )
    async with get_async_client() as client:
        response = await client.post(
            url="api/v1/documents",
            json=json.loads(body.json())
        )
        assert response.status_code == 200
        result: Result[Document] = Result[Document](**response.json())
        assert content.data.name == body.name
        assert content.data.description == body.description
        assert content.data.account_id == body.account_id
        assert content.data.document_type_id == body.document_type_id
        document_mock_data.data.append(content.data)


@pytest.mark.asyncio
async def test__patch_one_by_id__should_patch_one_document__success():
    body: PatchOneBody = PatchOneBody(
        name=f"{document_mock_data.data[0].name} patched",
        description=f"{document_mock_data.data[0].description} patched",
        account_id=document_mock_data.account_mock_data.data[1].id,
        document_type_id=document_mock_data.document_type_mock_data.data[1].id
    )
    async with get_async_client() as client:
        response = await client.patch(
            url=f"api/v1/documents/{document_mock_data.data[0].id}",
            json=json.loads(body.json())
        )
        assert response.status_code == 200
        result: Result[Document] = Result[Document](**response.json())
        assert content.data.name == body.name
        assert content.data.description == body.description
        assert content.data.account_id == body.account_id
        assert content.data.document_type_id == body.document_type_id
        document_mock_data.data[0] = content.data


@pytest.mark.asyncio
async def test__delete_one_by_id__should_delete_one_document__success():
    async with get_async_client() as client:
        response = await client.delete(
            url=f"api/v1/documents/{document_mock_data.data[0].id}"
        )
        assert response.status_code == 200
        result: Result[Document] = Result[Document](**response.json())
        assert content.data == document_mock_data.data[0]
