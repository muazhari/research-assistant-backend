import json
from typing import List

import pytest as pytest
import pytest_asyncio

from app.inners.models.entities.account import Account
from app.inners.models.entities.document import Document
from app.inners.models.entities.document_type import DocumentType
from app.inners.models.entities.file_document import FileDocument
from app.inners.models.value_objects.contracts.requests.managements.file_documents.create_body import \
    CreateBody
from app.inners.models.value_objects.contracts.requests.managements.file_documents.patch_body import \
    PatchBody
from app.inners.models.value_objects.contracts.responses.content import Content
from app.inners.models.value_objects.contracts.responses.managements.documents.file_document_response import \
    FileDocumentResponse
from app.outers.repositories.file_document_repository import FileDocumentRepository
from test.app.outers.interfaces.deliveries.controllers.account_controller_test import account_repository
from test.app.outers.interfaces.deliveries.controllers.document_controller_test import document_repository
from test.app.outers.interfaces.deliveries.controllers.document_type_controller_test import document_type_repository
from test.mock_data.file_document_mock_data import FileDocumentMockData
from test.utilities.test_client_utility import get_async_client

test_client = get_async_client()
file_document_repository = FileDocumentRepository()
file_document_mock_data = FileDocumentMockData()


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
        await document_repository.delete_one_by_id(document.id)
    for document_type in file_document_mock_data.document_mock_data.document_type_mock_data.data:
        await document_type_repository.delete_one_by_id(document_type.id)
    for account in file_document_mock_data.document_mock_data.account_mock_data.data:
        await account_repository.delete_one_by_id(account.id)


@pytest.mark.asyncio
async def test__read_all__should_return_all_file_documents__success():
    response = await test_client.get(
        url="api/v1/documents/files"
    )
    assert response.status_code == 200
    content: Content[List[FileDocumentResponse]] = Content[List[FileDocumentResponse]](**response.json())
    assert all(
        file_document_response in content.data
        for file_document_response in file_document_mock_data.response_data
    )


@pytest.mark.asyncio
async def test__read_one_by_id__should_return_one_file_document__success():
    response = await test_client.get(
        url=f"api/v1/documents/files/{file_document_mock_data.data[0].id}"
    )
    assert response.status_code == 200
    content: Content[FileDocumentResponse] = Content[FileDocumentResponse](**response.json())
    assert content.data == file_document_mock_data.response_data[0]


@pytest.mark.asyncio
async def test__create_one__should_create_one_file_document__success():
    body: CreateBody = CreateBody(
        name="name_3",
        description="description_3",
        document_type_id=file_document_mock_data.document_mock_data.document_type_mock_data.data[0].id,
        account_id=file_document_mock_data.document_mock_data.account_mock_data.data[0].id,
        file_name="file_name_3",
        file_extension="file_extension_3",
        file_bytes=b"file_bytes_3",
    )
    response = await test_client.post(
        url="api/v1/documents/files",
        json=json.loads(body.json())
    )
    assert response.status_code == 200
    content: Content[FileDocumentResponse] = Content[FileDocumentResponse](**response.json())
    assert content.data.name == body.name
    assert content.data.description == body.description
    assert content.data.document_type_id == body.document_type_id
    assert content.data.account_id == body.account_id
    assert content.data.file_name == body.file_name
    assert content.data.file_extension == body.file_extension
    assert content.data.file_bytes == body.file_bytes

    file_document_mock_data.response_data.append(content.data)
    file_document_mock_data.data.append(
        await file_document_repository.read_one_by_document_id(document_id=content.data.id)
    )
    file_document_mock_data.document_mock_data.data.append(
        await document_repository.read_one_by_id(id=content.data.id)
    )


@pytest.mark.asyncio
async def test__patch_one_by_id__should_patch_one_file_document__success():
    body: PatchBody = PatchBody(
        name=f"{file_document_mock_data.document_mock_data.data[0].name} patched",
        description=f"{file_document_mock_data.document_mock_data.data[0].description} patched",
        document_type_id=file_document_mock_data.document_mock_data.document_type_mock_data.data[1].id,
        account_id=file_document_mock_data.document_mock_data.account_mock_data.data[1].id,
        file_name=f"{file_document_mock_data.data[0].file_name} patched",
        file_extension=f"{file_document_mock_data.data[0].file_extension} patched",
        file_bytes=b"file_bytes_3 patched",
    )
    response = await test_client.patch(
        url=f"api/v1/documents/files/{file_document_mock_data.data[0].id}",
        json=json.loads(body.json())
    )
    assert response.status_code == 200
    content: Content[FileDocumentResponse] = Content[FileDocumentResponse](**response.json())
    assert content.data.name == body.name
    assert content.data.description == body.description
    assert content.data.document_type_id == body.document_type_id
    assert content.data.account_id == body.account_id
    assert content.data.file_name == body.file_name
    assert content.data.file_extension == body.file_extension
    assert content.data.file_bytes == body.file_bytes

    file_document_mock_data.response_data[0] = content.data
    file_document_mock_data.data[0] = await file_document_repository.read_one_by_document_id(
        document_id=content.data.id)
    file_document_mock_data.document_mock_data.data[0] = await document_repository.read_one_by_id(id=content.data.id)


@pytest.mark.asyncio
async def test__delete_one_by_id__should_delete_one_file_document__success():
    response = await test_client.delete(
        url=f"api/v1/documents/files/{file_document_mock_data.data[0].id}"
    )
    assert response.status_code == 200
    content: Content[FileDocumentResponse] = Content[FileDocumentResponse](**response.json())
    assert content.data == file_document_mock_data.data[0]
