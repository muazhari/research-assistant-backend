import json
import uuid
from datetime import datetime, timedelta

import pytest as pytest
import pytest_asyncio
from httpx import Response

from app.inners.models.daos.account import Account
from app.inners.models.daos.document import Document
from app.inners.models.daos.document_process import DocumentProcess
from app.inners.models.dtos.contracts.content import Content
from app.inners.models.dtos.contracts.requests.managements.document_processes.create_one_body import \
    CreateOneBody
from app.inners.models.dtos.contracts.requests.managements.document_processes.patch_one_body import \
    PatchOneBody
from test.containers.test_container import TestContainer
from test.main import MainTest

url_path: str = "/api/document-processes"


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
async def test__find_one_by_id__should_return_one_document_process__succeed(run_around: MainTest):
    selected_document_process_mock: DocumentProcess = \
        run_around.all_seeder.document_process_seeder.document_process_mock.data[0]
    response: Response = await run_around.client.get(
        url=f"{url_path}/{selected_document_process_mock.id}"
    )
    assert response.status_code == 200
    response_body: Content[DocumentProcess] = Content[DocumentProcess](**response.json())
    assert response_body.data == selected_document_process_mock


@pytest.mark.asyncio
async def test__create_one__should_create_one_document_process__succeed(run_around: MainTest):
    selected_account_mock: Account = run_around.all_seeder.document_seeder.document_mock.account_mock.data[0]
    selected_document_type_mock_initial = run_around.all_seeder.document_type_seeder.document_type_mock.data[0]
    selected_document_type_mock_final = run_around.all_seeder.document_type_seeder.document_type_mock.data[1]
    selected_document_mock_initial: Document = Document(
        id=uuid.uuid4(),
        name=f"name{uuid.uuid4()}",
        description=f"description{uuid.uuid4()}",
        document_type_id=selected_document_type_mock_initial.id,
        account_id=selected_account_mock.id,
    )
    await run_around.all_seeder.up_one_document(selected_document_mock_initial)
    selected_document_mock_final: Document = Document(
        id=uuid.uuid4(),
        name=f"name{uuid.uuid4()}",
        description=f"description{uuid.uuid4()}",
        document_type_id=selected_document_type_mock_final.id,
        account_id=selected_account_mock.id,
    )
    await run_around.all_seeder.up_one_document(selected_document_mock_final)
    current_time = datetime.now()
    started_at = current_time + timedelta(minutes=0)
    finished_at = current_time + timedelta(minutes=1)
    document_process_to_create_body: CreateOneBody = CreateOneBody(
        initial_document_id=selected_document_mock_initial.id,
        final_document_id=selected_document_mock_final.id,
        started_at=started_at,
        finished_at=finished_at,
    )
    response: Response = await run_around.client.post(
        url=url_path,
        json=json.loads(document_process_to_create_body.json())
    )
    assert response.status_code == 201
    response_body: Content[DocumentProcess] = Content[DocumentProcess](**response.json())
    assert response_body.data.initial_document_id == document_process_to_create_body.initial_document_id
    assert response_body.data.final_document_id == document_process_to_create_body.final_document_id
    assert response_body.data.started_at == document_process_to_create_body.started_at
    assert response_body.data.finished_at == document_process_to_create_body.finished_at


@pytest.mark.asyncio
async def test__patch_one_by_id__should_patch_one_document_process__succeed(run_around: MainTest):
    selected_document_process_mock: DocumentProcess = \
        run_around.all_seeder.document_process_seeder.document_process_mock.data[0]
    selected_document_mock_initial: Document = run_around.all_seeder.document_seeder.document_mock.data[0]
    selected_document_mock_final: Document = run_around.all_seeder.document_seeder.document_mock.data[1]
    current_time = datetime.now()
    started_at = current_time + timedelta(minutes=0)
    finished_at = current_time + timedelta(minutes=1)
    document_process_to_patch_body: PatchOneBody = PatchOneBody(
        initial_document_id=selected_document_mock_final.id,
        final_document_id=selected_document_mock_initial.id,
        started_at=started_at,
        finished_at=finished_at,
    )
    response: Response = await run_around.client.patch(
        url=f"{url_path}/{selected_document_process_mock.id}",
        json=json.loads(document_process_to_patch_body.json())
    )
    assert response.status_code == 200
    response_body: Content[DocumentProcess] = Content[DocumentProcess](**response.json())
    assert response_body.data.id == selected_document_process_mock.id
    assert response_body.data.initial_document_id == document_process_to_patch_body.initial_document_id
    assert response_body.data.final_document_id == document_process_to_patch_body.final_document_id
    assert response_body.data.started_at == document_process_to_patch_body.started_at
    assert response_body.data.finished_at == document_process_to_patch_body.finished_at


@pytest.mark.asyncio
async def test__delete_one_by_id__should_delete_one_document_process__succeed(run_around: MainTest):
    selected_document_process_mock: DocumentProcess = \
        run_around.all_seeder.document_process_seeder.document_process_mock.data[0]
    response: Response = await run_around.client.delete(
        url=f"{url_path}/{selected_document_process_mock.id}"
    )
    assert response.status_code == 200
    response_body: Content[DocumentProcess] = Content[DocumentProcess](**response.json())
    assert response_body.data == selected_document_process_mock
    run_around.all_seeder.delete_document_process_by_id_cascade(selected_document_process_mock.id)
