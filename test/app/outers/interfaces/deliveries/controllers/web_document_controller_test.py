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
from app.inners.models.value_objects.contracts.responses.managements.documents.web_document_response import \
    WebDocumentResponse
from app.outers.repositories.web_document_repository import WebDocumentRepository
from test.app.outers.interfaces.deliveries.controllers.account_controller_test import account_repository
from test.app.outers.interfaces.deliveries.controllers.document_controller_test import document_repository
from test.app.outers.interfaces.deliveries.controllers.document_type_controller_test import document_type_repository
from test.mock_data.web_document_mock_data import WebDocumentMockData
from test.utilities.test_client_utility import get_async_client

test_client = get_async_client()
web_document_repository = WebDocumentRepository()
web_document_mock_data = WebDocumentMockData()


@pytest_asyncio.fixture(scope="function", autouse=True)
async def run_around(request: pytest.FixtureRequest):
    for account in web_document_mock_data.document_mock_data.account_mock_data.data:
        await account_repository.create_one(Account(**account.dict()))
    for document_type in web_document_mock_data.document_mock_data.document_type_mock_data.data:
        await document_type_repository.create_one(DocumentType(**document_type.dict()))
    for document in web_document_mock_data.document_mock_data.data:
        await document_repository.create_one(Document(**document.dict()))
    for web_document in web_document_mock_data.data:
        await web_document_repository.create_one(WebDocument(**web_document.dict()))

    yield

    for web_document in web_document_mock_data.data:
        if request.node.name == "test__delete_one_by_id__should_delete_one_web_document__success" \
                and web_document.id == web_document_mock_data.data[0].id:
            continue
        await web_document_repository.delete_one_by_id(web_document.id)
    for document in web_document_mock_data.document_mock_data.data:
        await document_repository.delete_one_by_id(document.id)
    for document_type in web_document_mock_data.document_mock_data.document_type_mock_data.data:
        await document_type_repository.delete_one_by_id(document_type.id)
    for account in web_document_mock_data.document_mock_data.account_mock_data.data:
        await account_repository.delete_one_by_id(account.id)


@pytest.mark.asyncio
async def test__read_all__should_return_all_web_documents__success():
    response = await test_client.get(
        url="api/v1/documents/webs"
    )
    assert response.status_code == 200
    content: Content[List[WebDocumentResponse]] = Content[List[WebDocumentResponse]](**response.json())
    assert all(
        web_document_response in content.data
        for web_document_response in web_document_mock_data.response_data
    )


@pytest.mark.asyncio
async def test__read_one_by_id__should_return_one_web_document__success():
    response = await test_client.get(
        url=f"api/v1/documents/webs/{web_document_mock_data.data[0].id}"
    )
    assert response.status_code == 200
    content: Content[WebDocumentResponse] = Content[WebDocumentResponse](**response.json())
    assert content.data == web_document_mock_data.response_data[0]


@pytest.mark.asyncio
async def test__create_one__should_create_one_web_document__success():
    body: CreateBody = CreateBody(
        name="name_3",
        description="description_3",
        document_type_id=web_document_mock_data.document_mock_data.document_type_mock_data.data[0].id,
        account_id=web_document_mock_data.document_mock_data.account_mock_data.data[0].id,
        web_url="web_url_3"
    )
    response = await test_client.post(
        url="api/v1/documents/webs",
        json=json.loads(body.json())
    )
    assert response.status_code == 200
    content: Content[WebDocumentResponse] = Content[WebDocumentResponse](**response.json())
    assert content.data.name == body.name
    assert content.data.description == body.description
    assert content.data.document_type_id == body.document_type_id
    assert content.data.account_id == body.account_id
    assert content.data.web_url == body.web_url

    web_document_mock_data.response_data.append(content.data)
    web_document_mock_data.data.append(
        await web_document_repository.read_one_by_document_id(document_id=content.data.id)
    )
    web_document_mock_data.document_mock_data.data.append(
        await document_repository.read_one_by_id(id=content.data.id)
    )


@pytest.mark.asyncio
async def test__patch_one_by_id__should_patch_one_web_document__success():
    body: PatchBody = PatchBody(
        name=f"{web_document_mock_data.document_mock_data.data[0].name} patched",
        description=f"{web_document_mock_data.document_mock_data.data[0].description} patched",
        document_type_id=web_document_mock_data.document_mock_data.document_type_mock_data.data[1].id,
        account_id=web_document_mock_data.document_mock_data.account_mock_data.data[1].id,
        web_url=f"{web_document_mock_data.data[0].web_url} patched"
    )
    response = await test_client.patch(
        url=f"api/v1/documents/webs/{web_document_mock_data.data[0].id}",
        json=json.loads(body.json())
    )
    assert response.status_code == 200
    content: Content[WebDocumentResponse] = Content[WebDocumentResponse](**response.json())
    assert content.data.name == body.name
    assert content.data.description == body.description
    assert content.data.document_type_id == body.document_type_id
    assert content.data.account_id == body.account_id
    assert content.data.web_url == body.web_url

    web_document_mock_data.response_data[0] = content.data
    web_document_mock_data.data[0] = await web_document_repository.read_one_by_document_id(document_id=content.data.id)
    web_document_mock_data.document_mock_data.data[0] = await document_repository.read_one_by_id(id=content.data.id)


@pytest.mark.asyncio
async def test__delete_one_by_id__should_delete_one_web_document__success():
    response = await test_client.delete(
        url=f"api/v1/documents/webs/{web_document_mock_data.data[0].id}"
    )
    assert response.status_code == 200
    content: Content[WebDocumentResponse] = Content[WebDocumentResponse](**response.json())
    assert content.data == web_document_mock_data.data[0]
