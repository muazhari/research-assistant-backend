import hashlib
import json
import uuid

import pytest as pytest
import pytest_asyncio
from httpx import Response

from app.inners.models.daos.account import Account
from app.inners.models.daos.document import Document
from app.inners.models.daos.file_document import FileDocument
from app.inners.models.dtos.contracts.content import Content
from app.inners.models.dtos.contracts.requests.managements.file_documents.create_one_body import \
    CreateOneBody
from app.inners.models.dtos.contracts.requests.managements.file_documents.patch_one_body import \
    PatchOneBody
from app.inners.models.dtos.contracts.responses.managements.documents.file_document_response import FileDocumentResponse
from test.containers.test_container import TestContainer
from test.main import MainTest

url_path: str = "api/file-documents"


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
async def test__find_one_by_id__should_return_one_file_document__succeed(run_around: MainTest):
    selected_document_mock: Document = run_around.all_seeder.document_seeder.document_mock.data[0]
    selected_file_document_mock: FileDocument = run_around.all_seeder.file_document_seeder.file_document_mock.data[0]
    response: Response = await run_around.client.get(
        url=f"{url_path}/{selected_file_document_mock.id}"
    )
    assert response.status_code == 200
    response_body: Content[FileDocumentResponse] = Content[FileDocumentResponse](**response.json())
    assert response_body.data.id == selected_file_document_mock.id
    assert response_body.data.document_name == selected_document_mock.name
    assert response_body.data.document_description == selected_document_mock.description
    assert response_body.data.document_type_id == selected_document_mock.document_type_id
    assert response_body.data.document_account_id == selected_document_mock.account_id
    assert response_body.data.file_name == selected_file_document_mock.file_name
    assert response_body.data.file_extension == selected_file_document_mock.file_extension
    assert response_body.data.file_data_hash == selected_file_document_mock.file_data_hash
    assert response_body.data.file_meta == dict()


@pytest.mark.asyncio
async def test__create_one__should_create_one_file_document__succeed(run_around: MainTest):
    selected_document_mock: Document = run_around.all_seeder.document_seeder.document_mock.data[0]
    selected_document_type_mock: Document = run_around.all_seeder.document_seeder.document_mock.data[0]
    selected_account_mock: Account = run_around.all_seeder.document_seeder.document_mock.account_mock.data[0]
    selected_file_document_mock: FileDocument = run_around.all_seeder.file_document_seeder.file_document_mock.data[0]
    file_document_to_create_body: CreateOneBody = CreateOneBody(
        name=f"name{uuid.uuid4()}",
        description=f"description{uuid.uuid4()}",
        document_id=selected_document_mock.id,
        document_type_id=selected_document_type_mock.id,
        account_id=selected_account_mock.id,
        file_name=f"file_name{uuid.uuid4()}",
        file_extension=selected_file_document_mock.file_extension,
        file_data=selected_file_document_mock.file_data
    )
    response: Response = await run_around.client.post(
        url=url_path,
        json=json.loads(file_document_to_create_body.json())
    )
    assert response.status_code == 201
    response_body: Content[FileDocumentResponse] = Content[FileDocumentResponse](**response.json())
    assert response_body.data.document_name == file_document_to_create_body.name
    assert response_body.data.document_description == file_document_to_create_body.description
    assert response_body.data.document_type_id == file_document_to_create_body.document_type_id
    assert response_body.data.document_account_id == file_document_to_create_body.account_id
    assert response_body.data.file_name == file_document_to_create_body.file_name
    assert response_body.data.file_extension == file_document_to_create_body.file_extension
    assert response_body.data.file_data_hash == hashlib.sha256(file_document_to_create_body.file_data).hexdigest()
    assert response_body.data.file_meta == dict()


@pytest.mark.asyncio
async def test__patch_one_by_id__should_patch_one_file_document__succeed(run_around: MainTest):
    selected_file_document_mock: FileDocument = run_around.all_seeder.file_document_seeder.file_document_mock.data[0]
    selected_document_mock: Document = run_around.all_seeder.document_seeder.document_mock.data[0]
    selected_document_type_mock: Document = run_around.all_seeder.document_seeder.document_mock.data[0]
    selected_account_mock: Account = run_around.all_seeder.document_seeder.document_mock.account_mock.data[0]
    file_document_to_patch_body: PatchOneBody = PatchOneBody(
        name=f"patched.name{uuid.uuid4()}",
        description=f"patched.description{uuid.uuid4()}",
        document_id=selected_document_mock.id,
        document_type_id=selected_document_type_mock.id,
        account_id=selected_account_mock.id,
        file_name=f"patched.file_name{uuid.uuid4()}",
        file_extension=selected_file_document_mock.file_extension,
        file_data=selected_file_document_mock.file_data
    )
    response: Response = await run_around.client.patch(
        url=f"{url_path}/{selected_file_document_mock.id}",
        json=json.loads(file_document_to_patch_body.json())
    )
    assert response.status_code == 200
    response_body: Content[FileDocumentResponse] = Content[FileDocumentResponse](**response.json())
    assert response_body.data.document_name == file_document_to_patch_body.name
    assert response_body.data.document_description == file_document_to_patch_body.description
    assert response_body.data.document_type_id == file_document_to_patch_body.document_type_id
    assert response_body.data.document_account_id == file_document_to_patch_body.account_id
    assert response_body.data.file_name == file_document_to_patch_body.file_name
    assert response_body.data.file_extension == file_document_to_patch_body.file_extension
    assert response_body.data.file_data_hash == hashlib.sha256(file_document_to_patch_body.file_data).hexdigest()
    assert response_body.data.file_meta == dict()


@pytest.mark.asyncio
async def test__delete_one_by_id__should_delete_one_file_document__succeed(run_around: MainTest):
    selected_document_mock: Document = run_around.all_seeder.document_seeder.document_mock.data[0]
    selected_file_document_mock: FileDocument = run_around.all_seeder.file_document_seeder.file_document_mock.data[0]
    response: Response = await run_around.client.delete(
        url=f"{url_path}/{selected_file_document_mock.id}"
    )
    assert response.status_code == 200
    response_body: Content[FileDocumentResponse] = Content[FileDocumentResponse](**response.json())
    assert response_body.data.id == selected_file_document_mock.id
    assert response_body.data.document_name == selected_document_mock.name
    assert response_body.data.document_description == selected_document_mock.description
    assert response_body.data.document_type_id == selected_document_mock.document_type_id
    assert response_body.data.document_account_id == selected_document_mock.account_id
    assert response_body.data.file_name == selected_file_document_mock.file_name
    assert response_body.data.file_extension == selected_file_document_mock.file_extension
    assert response_body.data.file_data_hash == selected_file_document_mock.file_data_hash
    assert response_body.data.file_meta == dict()
    run_around.all_seeder.delete_file_document_by_id_cascade(selected_file_document_mock.id)