import json
from typing import List

import pytest as pytest
import pytest_asyncio

from app.inners.models.entities.account import Account
from app.inners.models.entities.document import Document
from app.inners.models.entities.document_type import DocumentType
from app.inners.models.entities.web_document import WebDocument
from app.inners.models.value_objects.contracts.requests.managements.web_documents.create_body import \
    CreateBody
from app.inners.models.value_objects.contracts.requests.managements.web_documents.patch_body import \
    PatchBody
from app.inners.models.value_objects.contracts.responses.content import Content
from app.outers.repositories.web_document_repository import WebDocumentRepository
from test.app.outers.interfaces.deliveries.controllers.account_controller_test import account_repository
from test.app.outers.interfaces.deliveries.controllers.document_controller_test import document_repository
from test.app.outers.interfaces.deliveries.controllers.document_type_controller_test import document_type_repository
from test.mock_data.web_document_mock_data import WebDocumentMockData
from test.utilities.test_client_utility import get_async_client

test_client = get_async_client()
web_document_repository = WebDocumentRepository()
web_document_mock_data = WebDocumentMockData()
data = web_document_mock_data.get_data()


@pytest_asyncio.fixture(scope="function", autouse=True)
async def run_around(request: pytest.FixtureRequest):
    for account in data["account"]:
        await account_repository.create_one(Account(**account.dict()))
    for document_type in data["document_type"]:
        await document_type_repository.create_one(DocumentType(**document_type.dict()))
    for document in data["document"]:
        await document_repository.create_one(Document(**document.dict()))
    for web_document in data["web_document"]:
        await web_document_repository.create_one(WebDocument(**web_document.dict()))

    yield

    for web_document in data["web_document"]:
        if request.node.name == "test__delete_one_by_id__should_delete_one_web_document__success" \
                and web_document.id == data["web_document"][0].id:
            continue
        await web_document_repository.delete_one_by_id(web_document.id)
    for document in data["document"]:
        await document_repository.delete_one_by_id(document.id)
    for document_type in data["document_type"]:
        await document_type_repository.delete_one_by_id(document_type.id)
    for account in data["account"]:
        await account_repository.delete_one_by_id(account.id)


@pytest.mark.asyncio
async def test__read_all__should_return_all_web_documents__success():
    response = await test_client.get(
        url="api/v1/documents/webs"
    )
    assert response.status_code == 200
    content: Content[List[WebDocument]] = Content[List[WebDocument]](**response.json())
    assert all([web_document in content.data for web_document in data["web_document"]])


@pytest.mark.asyncio
async def test__read_one_by_id__should_return_one_web_document__success():
    response = await test_client.get(
        url=f"api/v1/documents/webs/{data['web_document'][0].id}"
    )
    assert response.status_code == 200
    content: Content[WebDocument] = Content[WebDocument](**response.json())
    assert content.data == data["web_document"][0]


@pytest.mark.asyncio
async def test__create_one__should_create_one_web_document__success():
    web_document_create: CreateBody = CreateBody(
        document_id=data["document"][0].id,
        web_url="web_url_3",
    )
    response = await test_client.post(
        url="api/v1/documents/webs",
        json=json.loads(web_document_create.json())
    )
    assert response.status_code == 200
    content: Content[WebDocument] = Content[WebDocument](**response.json())
    assert content.data.document_id == web_document_create.document_id
    assert content.data.web_url == web_document_create.web_url

    data["web_document"].append(content.data)


@pytest.mark.asyncio
async def test__patch_one_by_id__should_patch_one_web_document__success():
    web_document_patch: PatchBody = PatchBody(
        document_id=data["document"][1].id,
        web_url=f"{data['web_document'][0].web_url} patched"
    )
    response = await test_client.patch(
        url=f"api/v1/documents/webs/{data['web_document'][0].id}",
        json=json.loads(web_document_patch.json())
    )
    assert response.status_code == 200
    content: Content[WebDocument] = Content[WebDocument](**response.json())
    assert content.data.document_id == web_document_patch.document_id
    assert content.data.web_url == web_document_patch.web_url
    data["web_document"][0] = content.data


@pytest.mark.asyncio
async def test__delete_one_by_id__should_delete_one_web_document__success():
    response = await test_client.delete(
        url=f"api/v1/documents/webs/{data['web_document'][0].id}"
    )
    assert response.status_code == 200
    content: Content[WebDocument] = Content[WebDocument](**response.json())
    assert content.data == data["web_document"][0]
