import json
from typing import List

import pytest as pytest
import pytest_asyncio
from test.utilities.test_client_utility import get_async_client

from app.inners.models.daos.account import Account
from app.inners.models.daos.document import Document
from app.inners.models.daos.document_type import DocumentType
from app.inners.models.daos.file_document import FileDocument
from app.inners.models.dtos.contracts.requests.managements.file_documents.create_one_body import \
    CreateOneBody
from app.inners.models.dtos.contracts.requests.managements.file_documents.patch_one_body import \
    PatchOneBody
from app.inners.models.dtos.contracts.responses.managements.documents.file_document_response import \
    FileDocumentResponse
from app.inners.models.dtos.contracts.result import Result
from app.outers.repositories.file_document_repository import FileDocumentRepository
from test.app.outers.interfaces.deliveries.controllers.account_controller_test import account_repository
from test.app.outers.interfaces.deliveries.controllers.document_controller_test import document_repository
from test.app.outers.interfaces.deliveries.controllers.document_type_controller_test import document_type_repository
from test.mocks.file_document_mock import FileDocumentMock

file_document_repository = FileDocumentRepository()
file_document_mock_data = FileDocumentMock()


@pytest_asyncio.fixture(scope="function", autouse=True)
async def run_around(request: pytest.FixtureRequest):
    for account in file_document_mock_data.document_mock_data.account_mock_data.data:
        await account_repository.create_one(Account(**account.dict()))
    for document_type in file_document_mock_data.document_mock_data.document_type_mock_data.data:
        await document_type_repository.create_one(DocumentType(**document_type.dict()))
    for document in file_document_mock_data.document_mock_data.data:
        await document_repository.create_one(Document(**document.dict()))
    for file_document in file_document_mock_data.data:
        await file_document_repository.create_one(FileDocument(**file_document.dict()))

    yield

    for file_document in file_document_mock_data.data:
        if request.node.name == "test__delete_one_by_id__should_delete_one_file_document__success" \
                and file_document.id == file_document_mock_data.data[0].id:
            continue
        await file_document_repository.delete_one_by_id(file_document.id)
    for document in file_document_mock_data.document_mock_data.data:
        if request.node.name == "test__delete_one_by_id__should_delete_one_file_document__success" \
                and document.id == file_document_mock_data.document_mock_data.data[0].id:
            continue
        await document_repository.delete_one_by_id(document.id)
    for document_type in file_document_mock_data.document_mock_data.document_type_mock_data.data:
        await document_type_repository.delete_one_by_id(document_type.id)
    for account in file_document_mock_data.document_mock_data.account_mock_data.data:
        await account_repository.delete_one_by_id(account.id)


@pytest.mark.asyncio
async def test__find_many__should_return_all_file_documents__success():
    async with get_async_client() as client:
        response = await client.get(
            url="api/v1/documents/files"
        )
        assert response.status_code == 200
        result: Result[List[FileDocumentResponse]] = Result[List[FileDocumentResponse]](**response.json())
        assert all(
            file_document_response in content.data
            for file_document_response in file_document_mock_data.response_data
        )


@pytest.mark.asyncio
async def test__find_one_by_id__should_return_one_file_document__success():
    async with get_async_client() as client:
        response = await client.get(
            url=f"api/v1/documents/files/{file_document_mock_data.data[0].id}"
        )
        assert response.status_code == 200
        result: Result[FileDocumentResponse] = Result[FileDocumentResponse](**response.json())
        assert content.data == file_document_mock_data.response_data[0]


@pytest.mark.asyncio
async def test__create_one__should_create_one_file_document__success():
    body: CreateOneBody = CreateOneBody(
        name="name_3",
        description="description_3",
        document_type_id=file_document_mock_data.document_mock_data.document_type_mock_data.data[0].id,
        account_id=file_document_mock_data.document_mock_data.account_mock_data.data[0].id,
        file_name="file_name_3",
        file_extension="file_extension_3",
        file_data=b"file_data_3",
    )
    async with get_async_client() as client:
        response = await client.post(
            url="api/v1/documents/files",
            json=json.loads(body.json())
        )
        assert response.status_code == 200
        result: Result[FileDocumentResponse] = Result[FileDocumentResponse](**response.json())
        assert content.data.name == body.name
        assert content.data.description == body.description
        assert content.data.document_type_id == body.document_type_id
        assert content.data.account_id == body.account_id
        assert content.data.file_name == body.file_name
        assert content.data.file_extension == body.file_extension
        assert content.data.file_data == body.file_data

        file_document_mock_data.response_data.append(content.data)
        file_document_mock_data.data.append(
            await file_document_repository.find_one_by_document_id(document_id=content.data.id)
        )
        file_document_mock_data.document_mock_data.data.append(
            await document_repository.find_one_by_id(id=content.data.id)
        )


@pytest.mark.asyncio
async def test__patch_one_by_id__should_patch_one_file_document__success():
    body: PatchOneBody = PatchOneBody(
        name=f"{file_document_mock_data.document_mock_data.data[0].name} patched",
        description=f"{file_document_mock_data.document_mock_data.data[0].description} patched",
        document_type_id=file_document_mock_data.document_mock_data.document_type_mock_data.data[1].id,
        account_id=file_document_mock_data.document_mock_data.account_mock_data.data[1].id,
        file_name=f"{file_document_mock_data.data[0].file_name} patched",
        file_extension=f"{file_document_mock_data.data[0].file_extension} patched",
        file_data=b"file_data_3 patched",
    )
    async with get_async_client() as client:
        response = await client.patch(
            url=f"api/v1/documents/files/{file_document_mock_data.response_data[0].id}",
            json=json.loads(body.json())
        )
        assert response.status_code == 200
        result: Result[FileDocumentResponse] = Result[FileDocumentResponse](**response.json())
        assert content.data.name == body.name
        assert content.data.description == body.description
        assert content.data.document_type_id == body.document_type_id
        assert content.data.account_id == body.account_id
        assert content.data.file_name == body.file_name
        assert content.data.file_extension == body.file_extension
        assert content.data.file_data == body.file_data

        file_document_mock_data.response_data[0] = content.data
        file_document_mock_data.data[0] = await file_document_repository.find_one_by_document_id(
            document_id=content.data.id)
        file_document_mock_data.document_mock_data.data[0] = await document_repository.find_one_by_id(
            id=content.data.id)


@pytest.mark.asyncio
async def test__delete_one_by_id__should_delete_one_file_document__success():
    async with get_async_client() as client:
        response = await client.delete(
            url=f"api/v1/documents/files/{file_document_mock_data.response_data[0].id}"
        )
        assert response.status_code == 200
        result: Result[FileDocumentResponse] = Result[FileDocumentResponse](**response.json())
        assert content.data == file_document_mock_data.response_data[0]
