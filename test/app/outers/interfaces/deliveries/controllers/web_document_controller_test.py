import hashlib
import json
import uuid

import pytest as pytest
import pytest_asyncio
from httpx import Response

from app.inners.models.daos.account import Account
from app.inners.models.daos.document import Document
from app.inners.models.daos.web_document import WebDocument
from app.inners.models.dtos.contracts.content import Content
from app.inners.models.dtos.contracts.requests.managements.web_documents.create_one_body import \
    CreateOneBody
from app.inners.models.dtos.contracts.requests.managements.web_documents.patch_one_body import \
    PatchOneBody
from app.inners.models.dtos.contracts.responses.managements.documents.web_document_response import WebDocumentResponse
from test.containers.test_container import TestContainer
from test.main import MainTest

url_path = "api/v1/web_documents"


@pytest_asyncio.fixture(scope="function", autouse=True)
async def run_around(request: pytest.FixtureRequest):
    test_container: TestContainer = TestContainer()
    main_test = MainTest(
        all_seeder=test_container.seeders.all_seeder()
    )
    await main_test.all_seeder.up()
    yield main_test
    await main_test.all_seeder.down()


@pytest.mark.asyncio
async def test__find_one_by_id__should_return_one_web_document__succeed(run_around: MainTest):
    selected_document_mock: Document = run_around.all_seeder.document_seeder.document_mock.data[0]
    selected_web_document_mock: WebDocument = run_around.all_seeder.web_document_seeder.web_document_mock.data[0]
    response: Response = await run_around.client.get(
        url=f"{url_path}/{selected_web_document_mock.id}"
    )
    assert response.status_code == 200
    response_body: Content[WebDocumentResponse] = Content[WebDocumentResponse](**response.json())
    assert response_body.data.id == selected_web_document_mock.id
    assert response_body.data.document_name == selected_document_mock.name
    assert response_body.data.document_description == selected_document_mock.description
    assert response_body.data.document_type_id == selected_document_mock.document_type_id
    assert response_body.data.document_account_id == selected_document_mock.account_id
    assert response_body.data.web_url == selected_web_document_mock.web_url
    assert response_body.data.web_url_hash == selected_web_document_mock.web_url_hash


@pytest.mark.asyncio
async def test__create_one__should_create_one_web_document__succeed(run_around: MainTest):
    selected_document_mock: Document = run_around.all_seeder.document_seeder.document_mock.data[0]
    selected_document_type_mock: Document = run_around.all_seeder.document_seeder.document_mock.data[0]
    selected_account_mock: Account = run_around.all_seeder.document_seeder.document_mock.account_mock.data[0]
    selected_web_document_mock: WebDocument = run_around.all_seeder.web_document_seeder.web_document_mock.data[0]
    web_document_to_create_body: CreateOneBody = CreateOneBody(
        name=f"name{uuid.uuid4()}",
        description=f"description{uuid.uuid4()}",
        document_id=selected_document_mock.id,
        document_type_id=selected_document_type_mock.id,
        account_id=selected_account_mock.id,
        web_url=selected_web_document_mock.web_url,
        web_url_hash=selected_web_document_mock.web_url_hash
    )
    response: Response = await run_around.client.post(
        url=url_path,
        data=json.loads(web_document_to_create_body.json())
    )
    assert response.status_code == 201
    response_body: Content[WebDocumentResponse] = Content[WebDocumentResponse](**response.json())
    assert response_body.data.document_name == web_document_to_create_body.name
    assert response_body.data.document_description == web_document_to_create_body.description
    assert response_body.data.document_type_id == web_document_to_create_body.document_type_id
    assert response_body.data.document_account_id == web_document_to_create_body.account_id
    assert response_body.data.web_url == web_document_to_create_body.web_url
    assert response_body.data.web_url_hash == hashlib.sha256(web_document_to_create_body.web_url.encode()).hexdigest()


@pytest.mark.asyncio
async def test__patch_one_by_id__should_patch_one_web_document__succeed(run_around: MainTest):
    selected_web_document_mock: WebDocument = run_around.all_seeder.web_document_seeder.web_document_mock.data[0]
    selected_document_mock: Document = run_around.all_seeder.document_seeder.document_mock.data[0]
    selected_document_type_mock: Document = run_around.all_seeder.document_seeder.document_mock.data[0]
    selected_account_mock: Account = run_around.all_seeder.document_seeder.document_mock.account_mock.data[0]
    web_document_to_patch_body: PatchOneBody = PatchOneBody(
        name=f"patched.name{uuid.uuid4()}",
        description=f"patched.description{uuid.uuid4()}",
        document_id=selected_document_mock.id,
        document_type_id=selected_document_type_mock.id,
        account_id=selected_account_mock.id,
        web_url=selected_web_document_mock.web_url,
        web_url_hash=selected_web_document_mock.web_url_hash
    )
    response: Response = await run_around.client.patch(
        url=f"{url_path}/{selected_web_document_mock.id}",
        data=json.loads(web_document_to_patch_body.json())
    )
    assert response.status_code == 200
    response_body: Content[WebDocumentResponse] = Content[WebDocumentResponse](**response.json())
    assert response_body.data.document_name == web_document_to_patch_body.name
    assert response_body.data.document_description == web_document_to_patch_body.description
    assert response_body.data.document_type_id == web_document_to_patch_body.document_type_id
    assert response_body.data.document_account_id == web_document_to_patch_body.account_id
    assert response_body.data.web_url == web_document_to_patch_body.web_url
    assert response_body.data.web_url_hash == hashlib.sha256(web_document_to_patch_body.web_url.encode()).hexdigest()


@pytest.mark.asyncio
async def test__delete_one_by_id__should_delete_one_web_document__succeed(run_around: MainTest):
    selected_document_mock: Document = run_around.all_seeder.document_seeder.document_mock.data[0]
    selected_web_document_mock: WebDocument = run_around.all_seeder.web_document_seeder.web_document_mock.data[0]
    response: Response = await run_around.client.delete(
        url=f"{url_path}/{selected_web_document_mock.id}"
    )
    assert response.status_code == 200
    response_body: Content[WebDocumentResponse] = Content[WebDocumentResponse](**response.json())
    assert response_body.data.id == selected_web_document_mock.id
    assert response_body.data.document_name == selected_document_mock.name
    assert response_body.data.document_description == selected_document_mock.description
    assert response_body.data.document_type_id == selected_document_mock.document_type_id
    assert response_body.data.document_account_id == selected_document_mock.account_id
    assert response_body.data.web_url == selected_web_document_mock.web_url
    assert response_body.data.web_url_hash == selected_web_document_mock.web_url_hash
