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
from app.outers.repositories.file_document_repository import FileDocumentRepository
from test.app.outers.interfaces.deliveries.controllers.account_controller_test import account_repository
from test.app.outers.interfaces.deliveries.controllers.document_controller_test import document_repository
from test.app.outers.interfaces.deliveries.controllers.document_type_controller_test import document_type_repository
from test.mock_data.file_document_mock_data import FileDocumentMockData
from test.utilities.test_client_utility import get_async_client

test_client = get_async_client()
file_document_repository = FileDocumentRepository()
file_document_mock_data = FileDocumentMockData()
data = file_document_mock_data.get_data()


@pytest_asyncio.fixture(scope="function", autouse=True)
async def run_around(request: pytest.FixtureRequest):
    for account in data["account"]:
        await account_repository.create_one(Account(**account.dict()))
    for document_type in data["document_type"]:
        await document_type_repository.create_one(DocumentType(**document_type.dict()))
    for document in data["document"]:
        await document_repository.create_one(Document(**document.dict()))
    for file_document in data["file_document"]:
        await file_document_repository.create_one(FileDocument(**file_document.dict()))

    yield

    for file_document in data["file_document"]:
        if request.node.name == "test__delete_one_by_id__should_delete_one_file_document__success" \
                and file_document.id == data["file_document"][0].id:
            continue
        await file_document_repository.delete_one_by_id(file_document.id)
    for document in data["document"]:
        await document_repository.delete_one_by_id(document.id)
    for document_type in data["document_type"]:
        await document_type_repository.delete_one_by_id(document_type.id)
    for account in data["account"]:
        await account_repository.delete_one_by_id(account.id)


@pytest.mark.asyncio
async def test__read_all__should_return_all_file_documents__success():
    response = await test_client.get(
        url="api/v1/documents/files"
    )
    assert response.status_code == 200
    content: Content[List[FileDocument]] = Content[List[FileDocument]](**response.json())
    assert all([file_document in content.data for file_document in data["file_document"]])


@pytest.mark.asyncio
async def test__read_one_by_id__should_return_one_file_document__success():
    response = await test_client.get(
        url=f"api/v1/documents/files/{data['file_document'][0].id}"
    )
    assert response.status_code == 200
    content: Content[FileDocument] = Content[FileDocument](**response.json())
    assert content.data == data["file_document"][0]


@pytest.mark.asyncio
async def test__create_one__should_create_one_file_document__success():
    file_document_create: CreateBody = CreateBody(
        document_id=data["document"][0].id,
        file_name="file_name_3",
        file_extension="file_extension_3",
        file_bytes=b"file_bytes_3",
    )
    response = await test_client.post(
        url="api/v1/documents/files",
        json=json.loads(file_document_create.json())
    )
    assert response.status_code == 200
    content: Content[FileDocument] = Content[FileDocument](**response.json())
    assert content.data.document_id == file_document_create.document_id
    assert content.data.file_name == file_document_create.file_name
    assert content.data.file_extension == file_document_create.file_extension
    data["file_document"].append(content.data)


@pytest.mark.asyncio
async def test__patch_one_by_id__should_patch_one_file_document__success():
    file_document_patch: PatchBody = PatchBody(
        document_id=data["document"][1].id,
        file_name=f"{data['file_document'][0].file_name} patched",
        file_extension=f"{data['file_document'][0].file_extension} patched",
        file_bytes=b"file_bytes_3 patched",
    )
    response = await test_client.patch(
        url=f"api/v1/documents/files/{data['file_document'][0].id}",
        json=json.loads(file_document_patch.json())
    )
    assert response.status_code == 200
    content: Content[FileDocument] = Content[FileDocument](**response.json())
    assert content.data.document_id == file_document_patch.document_id
    assert content.data.file_name == file_document_patch.file_name
    assert content.data.file_extension == file_document_patch.file_extension
    assert content.data.file_bytes == file_document_patch.file_bytes
    data["file_document"][0] = content.data


@pytest.mark.asyncio
async def test__delete_one_by_id__should_delete_one_file_document__success():
    response = await test_client.delete(
        url=f"api/v1/documents/files/{data['file_document'][0].id}"
    )
    assert response.status_code == 200
    content: Content[FileDocument] = Content[FileDocument](**response.json())
    assert content.data == data["file_document"][0]
