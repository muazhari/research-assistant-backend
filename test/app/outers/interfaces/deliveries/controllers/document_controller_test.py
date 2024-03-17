import json
import uuid

import pytest as pytest
import pytest_asyncio
from httpx import Response

from app.inners.models.daos.account import Account
from app.inners.models.daos.document import Document
from app.inners.models.dtos.contracts.content import Content
from app.inners.models.dtos.contracts.requests.managements.documents.create_one_body import \
    CreateOneBody
from test.containers.test_container import TestContainer
from test.main import MainTest

url_path = "api/documents"


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
async def test__find_one_by_id__should_return_one_document__succeed(run_around: MainTest):
    selected_document_mock: Document = run_around.all_seeder.document_seeder.document_mock.data[0]
    response: Response = await run_around.client.get(
        url=f"{url_path}/{selected_document_mock.id}"
    )
    assert response.status_code == 200
    response_body: Content[Document] = Content[Document](**response.json())
    assert response_body.data == selected_document_mock


@pytest.mark.asyncio
async def test__create_one__should_create_one_document__succeed(run_around: MainTest):
    selected_document_type_mock: Document = run_around.all_seeder.document_seeder.document_mock.data[0]
    selected_account_mock: Account = run_around.all_seeder.document_seeder.document_mock.account_mock.data[0]
    document_to_create_body: CreateOneBody = CreateOneBody(
        name=f"name{uuid.uuid4()}",
        description=f"description{uuid.uuid4()}",
        document_type_id=selected_document_type_mock.id,
        account_id=selected_account_mock.id
    )
    response: Response = await run_around.client.post(
        url=url_path,
        json=json.loads(document_to_create_body.json())
    )
    assert response.status_code == 201
    response_body: Content[Document] = Content[Document](**response.json())
    assert response_body.data.name == document_to_create_body.name
    assert response_body.data.description == document_to_create_body.description
    assert response_body.data.document_type_id == document_to_create_body.document_type_id
    assert response_body.data.account_id == document_to_create_body.account_id


@pytest.mark.asyncio
async def test__patch_one_by_id__should_patch_one_document__succeed(run_around: MainTest):
    selected_document_mock: Document = run_around.all_seeder.document_seeder.document_mock.data[0]
    selected_document_type_mock: Document = run_around.all_seeder.document_seeder.document_mock.data[0]
    selected_account_mock: Account = run_around.all_seeder.document_seeder.document_mock.account_mock.data[0]
    document_to_patch_body: CreateOneBody = CreateOneBody(
        name=f"patched.name{uuid.uuid4()}",
        description=f"patched.description{uuid.uuid4()}",
        document_type_id=selected_document_type_mock.id,
        account_id=selected_account_mock.id
    )
    response: Response = await run_around.client.patch(
        url=f"{url_path}/{selected_document_mock.id}",
        json=json.loads(document_to_patch_body.json())
    )
    assert response.status_code == 200
    response_body: Content[Document] = Content[Document](**response.json())
    assert response_body.data.id == selected_document_mock.id
    assert response_body.data.name == document_to_patch_body.name
    assert response_body.data.description == document_to_patch_body.description
    assert response_body.data.document_type_id == document_to_patch_body.document_type_id
    assert response_body.data.account_id == document_to_patch_body.account_id


@pytest.mark.asyncio
async def test__delete_one_by_id__should_delete_one_document__succeed(run_around: MainTest):
    selected_document_mock: Document = run_around.all_seeder.document_seeder.document_mock.data[0]
    response: Response = await run_around.client.delete(
        url=f"{url_path}/{selected_document_mock.id}"
    )
    assert response.status_code == 200
    response_body: Content[Document] = Content[Document](**response.json())
    assert response_body.data == selected_document_mock
    run_around.all_seeder.delete_document_by_id_cascade(selected_document_mock.id)
