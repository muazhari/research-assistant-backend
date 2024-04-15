import uuid
from datetime import datetime, timedelta, timezone
from typing import Dict, Any, List

import pytest as pytest
from httpx import Response
from starlette import status

from apps.inners.models.daos.account import Account
from apps.inners.models.daos.document import Document
from apps.inners.models.daos.document_process import DocumentProcess
from apps.inners.models.daos.session import Session
from apps.inners.models.dtos.content import Content
from apps.inners.models.dtos.contracts.requests.managements.document_processes.create_one_body import \
    CreateOneBody
from apps.inners.models.dtos.contracts.requests.managements.document_processes.patch_one_body import \
    PatchOneBody
from tests.main_context import MainContext

url_path: str = "/api/document-processes"


@pytest.mark.asyncio
async def test__find_many_with_pagination__should__succeed(main_context: MainContext):
    selected_session_fake: Session = main_context.all_seeder.session_seeder.session_fake.data[0]
    selected_document_process_fakes: List[DocumentProcess] = []
    for document_process_fake in main_context.all_seeder.document_process_seeder.document_process_fake.data:
        for document_fake in main_context.all_seeder.document_seeder.document_fake.data:
            if document_process_fake.initial_document_id == document_fake.id:
                if document_fake.account_id == selected_session_fake.account_id:
                    selected_document_process_fakes.append(document_process_fake)

    headers: Dict[str, Any] = {
        "Authorization": f"Bearer {selected_session_fake.access_token}"
    }
    params: Dict[str, Any] = {
        "page_number": 1,
        "page_size": len(selected_document_process_fakes)
    }
    response: Response = await main_context.client.get(
        url=url_path,
        headers=headers,
        params=params
    )
    content: Content[List[DocumentProcess]] = Content[List[DocumentProcess]](
        **response.json(),
        status_code=response.status_code
    )
    assert content.status_code == status.HTTP_200_OK
    assert len(content.data) == len(selected_document_process_fakes)
    for document_process in content.data:
        for selected_document_process_fake in selected_document_process_fakes:
            if document_process.id == selected_document_process_fake.id:
                assert document_process == selected_document_process_fake


@pytest.mark.asyncio
async def test__find_one_by_id__should__succeed(main_context: MainContext):
    selected_document_process_fake: DocumentProcess = \
        main_context.all_seeder.document_process_seeder.document_process_fake.data[0]
    selected_session_fake: Session = main_context.all_seeder.session_seeder.session_fake.data[0]
    headers: Dict[str, Any] = {
        "Authorization": f"Bearer {selected_session_fake.access_token}"
    }
    response: Response = await main_context.client.get(
        url=f"{url_path}/{selected_document_process_fake.id}",
        headers=headers
    )

    content: Content[DocumentProcess] = Content[DocumentProcess](
        **response.json(),
        status_code=response.status_code
    )
    assert content.status_code == status.HTTP_200_OK
    assert content.data == selected_document_process_fake


@pytest.mark.asyncio
async def test__create_one__should_create_one_document_process__succeed(main_context: MainContext):
    selected_account_fake: Account = main_context.all_seeder.document_seeder.document_fake.account_fake.data[0]
    selected_session_fake: Session = main_context.all_seeder.session_seeder.session_fake.data[0]
    selected_document_type_fake_initial = main_context.all_seeder.document_type_seeder.document_type_fake.data[0]
    selected_document_type_fake_final = main_context.all_seeder.document_type_seeder.document_type_fake.data[1]
    selected_document_fake_initial: Document = Document(
        id=uuid.uuid4(),
        name=f"name{uuid.uuid4()}",
        description=f"description{uuid.uuid4()}",
        document_type_id=selected_document_type_fake_initial.id,
        account_id=selected_account_fake.id,
    )
    await main_context.all_seeder.up_one_document(selected_document_fake_initial)
    selected_document_fake_final: Document = Document(
        id=uuid.uuid4(),
        name=f"name{uuid.uuid4()}",
        description=f"description{uuid.uuid4()}",
        document_type_id=selected_document_type_fake_final.id,
        account_id=selected_account_fake.id,
    )
    await main_context.all_seeder.up_one_document(selected_document_fake_final)
    current_time = datetime.now(tz=timezone.utc)
    started_at = current_time + timedelta(minutes=0)
    finished_at = current_time + timedelta(minutes=1)
    document_process_creator_body: CreateOneBody = CreateOneBody(
        initial_document_id=selected_document_fake_initial.id,
        final_document_id=selected_document_fake_final.id,
        started_at=started_at,
        finished_at=finished_at,
    )
    headers: Dict[str, Any] = {
        "Authorization": f"Bearer {selected_session_fake.access_token}"
    }
    response: Response = await main_context.client.post(
        url=url_path,
        json=document_process_creator_body.model_dump(mode="json"),
        headers=headers
    )

    content: Content[DocumentProcess] = Content[DocumentProcess](
        **response.json(),
        status_code=response.status_code
    )
    assert content.status_code == status.HTTP_201_CREATED
    assert content.data.initial_document_id == document_process_creator_body.initial_document_id
    assert content.data.final_document_id == document_process_creator_body.final_document_id
    assert content.data.started_at == document_process_creator_body.started_at
    assert content.data.finished_at == document_process_creator_body.finished_at

    main_context.all_seeder.document_process_seeder.document_process_fake.data.append(content.data)


@pytest.mark.asyncio
async def test__patch_one_by_id__should_patch_one_document_process__succeed(main_context: MainContext):
    selected_session_fake: Session = main_context.all_seeder.session_seeder.session_fake.data[0]
    selected_document_process_fake: DocumentProcess = \
        main_context.all_seeder.document_process_seeder.document_process_fake.data[0]
    selected_document_fake_initial: Document = main_context.all_seeder.document_seeder.document_fake.data[0]
    selected_document_fake_final: Document = main_context.all_seeder.document_seeder.document_fake.data[1]
    current_time = datetime.now(tz=timezone.utc)
    started_at = current_time + timedelta(minutes=0)
    finished_at = current_time + timedelta(minutes=1)
    document_process_patcher_body: PatchOneBody = PatchOneBody(
        initial_document_id=selected_document_fake_final.id,
        final_document_id=selected_document_fake_initial.id,
        started_at=started_at,
        finished_at=finished_at,
    )
    headers: Dict[str, Any] = {
        "Authorization": f"Bearer {selected_session_fake.access_token}"
    }
    response: Response = await main_context.client.patch(
        url=f"{url_path}/{selected_document_process_fake.id}",
        json=document_process_patcher_body.model_dump(mode="json"),
        headers=headers
    )

    content: Content[DocumentProcess] = Content[DocumentProcess](
        **response.json(),
        status_code=response.status_code
    )
    assert content.status_code == status.HTTP_200_OK
    assert content.data.id == selected_document_process_fake.id
    assert content.data.initial_document_id == document_process_patcher_body.initial_document_id
    assert content.data.final_document_id == document_process_patcher_body.final_document_id
    assert content.data.started_at == document_process_patcher_body.started_at
    assert content.data.finished_at == document_process_patcher_body.finished_at


@pytest.mark.asyncio
async def test__delete_one_by_id__should_delete_one_document_process__succeed(main_context: MainContext):
    selected_document_process_fake: DocumentProcess = \
        main_context.all_seeder.document_process_seeder.document_process_fake.data[0]
    selected_session_fake: Session = main_context.all_seeder.session_seeder.session_fake.data[0]
    headers: Dict[str, Any] = {
        "Authorization": f"Bearer {selected_session_fake.access_token}"
    }
    response: Response = await main_context.client.delete(
        url=f"{url_path}/{selected_document_process_fake.id}",
        headers=headers
    )

    content: Content[DocumentProcess] = Content[DocumentProcess](
        **response.json(),
        status_code=response.status_code
    )
    assert content.status_code == status.HTTP_200_OK
    assert content.data == selected_document_process_fake
    main_context.all_seeder.delete_many_document_process_by_id_cascade(selected_document_process_fake.id)
