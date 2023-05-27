import json
from typing import List

import pytest as pytest
import pytest_asyncio

from app.inners.models.entities.account import Account
from app.inners.models.entities.document import Document
from app.inners.models.entities.document_type import DocumentType
from app.inners.models.entities.text_document import TextDocument
from app.inners.models.value_objects.contracts.requests.managements.text_documents.create_body import \
    CreateBody
from app.inners.models.value_objects.contracts.requests.managements.text_documents.patch_body import \
    PatchBody
from app.inners.models.value_objects.contracts.responses.content import Content
from app.outers.repositories.text_document_repository import TextDocumentRepository
from test.app.outers.interfaces.deliveries.controllers.account_controller_test import account_repository
from test.app.outers.interfaces.deliveries.controllers.document_controller_test import document_repository
from test.app.outers.interfaces.deliveries.controllers.document_type_controller_test import document_type_repository
from test.mock_data.text_document_mock_data import TextDocumentMockData
from test.utilities.test_client_utility import get_async_client

test_client = get_async_client()
text_document_repository = TextDocumentRepository()
text_document_mock_data = TextDocumentMockData()
data = text_document_mock_data.get_data()


@pytest_asyncio.fixture(scope="function", autouse=True)
async def run_around(request: pytest.FixtureRequest):
    for account in data["account"]:
        await account_repository.create_one(Account(**account.dict()))
    for document_type in data["document_type"]:
        await document_type_repository.create_one(DocumentType(**document_type.dict()))
    for document in data["document"]:
        await document_repository.create_one(Document(**document.dict()))
    for text_document in data["text_document"]:
        await text_document_repository.create_one(TextDocument(**text_document.dict()))

    yield

    for text_document in data["text_document"]:
        if request.node.name == "test__delete_one_by_id__should_delete_one_text_document__success" \
                and text_document.id == data["text_document"][0].id:
            continue
        await text_document_repository.delete_one_by_id(text_document.id)
    for document in data["document"]:
        await document_repository.delete_one_by_id(document.id)
    for document_type in data["document_type"]:
        await document_type_repository.delete_one_by_id(document_type.id)
    for account in data["account"]:
        await account_repository.delete_one_by_id(account.id)


@pytest.mark.asyncio
async def test__read_all__should_return_all_text_documents__success():
    response = await test_client.get(
        url="api/v1/documents/texts"
    )
    assert response.status_code == 200
    content: Content[List[TextDocument]] = Content[List[TextDocument]](**response.json())
    assert all([text_document in content.data for text_document in data["text_document"]])


@pytest.mark.asyncio
async def test__read_one_by_id__should_return_one_text_document__success():
    response = await test_client.get(
        url=f"api/v1/documents/texts/{data['text_document'][0].id}"
    )
    assert response.status_code == 200
    content: Content[TextDocument] = Content[TextDocument](**response.json())
    assert content.data == data["text_document"][0]


@pytest.mark.asyncio
async def test__create_one__should_create_one_text_document__success():
    text_document_create: CreateBody = CreateBody(
        document_id=data["document"][0].id,
        text_content="text_content_3"
    )
    response = await test_client.post(
        url="api/v1/documents/texts",
        json=json.loads(text_document_create.json())
    )
    assert response.status_code == 200
    content: Content[TextDocument] = Content[TextDocument](**response.json())
    assert content.data.document_id == text_document_create.document_id
    assert content.data.text_content == text_document_create.text_content
    data["text_document"].append(content.data)


@pytest.mark.asyncio
async def test__patch_one_by_id__should_patch_one_text_document__success():
    text_document_patch: PatchBody = PatchBody(
        document_id=data["document"][1].id,
        text_content=f"{data['text_document'][0].text_content} patched"
    )
    response = await test_client.patch(
        url=f"api/v1/documents/texts/{data['text_document'][0].id}",
        json=json.loads(text_document_patch.json())
    )
    assert response.status_code == 200
    content: Content[TextDocument] = Content[TextDocument](**response.json())
    assert content.data.document_id == text_document_patch.document_id
    assert content.data.text_content == text_document_patch.text_content
    data["text_document"][0] = content.data


@pytest.mark.asyncio
async def test__delete_one_by_id__should_delete_one_text_document__success():
    response = await test_client.delete(
        url=f"api/v1/documents/texts/{data['text_document'][0].id}"
    )
    assert response.status_code == 200
    content: Content[TextDocument] = Content[TextDocument](**response.json())
    assert content.data == data["text_document"][0]
