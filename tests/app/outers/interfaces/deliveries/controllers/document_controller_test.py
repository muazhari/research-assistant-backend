import json
import uuid

import pytest as pytest
from httpx import Response
from starlette import status

from apps.inners.models.daos.account import Account
from apps.inners.models.daos.document import Document
from apps.inners.models.daos.document_type import DocumentType
from apps.inners.models.daos.session import Session
from apps.inners.models.dtos.content import Content
from apps.inners.models.dtos.contracts.requests.managements.documents.create_one_body import \
    CreateOneBody
from tests.main_context import MainContext

url_path: str = "/api/documents"


@pytest.mark.asyncio
async def test__find_one_by_id__should__succeed(main_context: MainContext):
    selected_document_fake: Document = main_context.all_seeder.document_seeder.document_fake.data[0]
    selected_session_fake: Session = main_context.all_seeder.session_seeder.session_fake.data[0]
    headers: dict = {
        "Authorization": f"Bearer {selected_session_fake.access_token}"
    }
    response: Response = await main_context.client.get(
        url=f"{url_path}/{selected_document_fake.id}",
        headers=headers
    )

    content: Content[Document] = Content[Document](
        **response.json(),
        status_code=response.status_code
    )
    assert content.status_code == status.HTTP_200_OK
    assert content.data == selected_document_fake


@pytest.mark.asyncio
async def test__create_one__should_create_one_document__succeed(main_context: MainContext):
    selected_document_type_fake: DocumentType = main_context.all_seeder.document_type_seeder.document_type_fake.data[0]
    selected_account_fake: Account = main_context.all_seeder.document_seeder.document_fake.account_fake.data[0]
    selected_session_fake: Session = main_context.all_seeder.session_seeder.session_fake.data[0]
    document_creator_body: CreateOneBody = CreateOneBody(
        name=f"name{uuid.uuid4()}",
        description=f"description{uuid.uuid4()}",
        document_type_id=selected_document_type_fake.id,
        account_id=selected_account_fake.id
    )
    headers: dict = {
        "Authorization": f"Bearer {selected_session_fake.access_token}"
    }
    response: Response = await main_context.client.post(
        url=url_path,
        json=json.loads(document_creator_body.json()),
        headers=headers
    )

    content: Content[Document] = Content[Document](
        **response.json(),
        status_code=response.status_code
    )
    assert content.status_code == status.HTTP_201_CREATED
    assert content.data.name == document_creator_body.name
    assert content.data.description == document_creator_body.description
    assert content.data.document_type_id == document_creator_body.document_type_id
    assert content.data.account_id == document_creator_body.account_id


@pytest.mark.asyncio
async def test__patch_one_by_id__should_patch_one_document__succeed(main_context: MainContext):
    selected_document_fake: Document = main_context.all_seeder.document_seeder.document_fake.data[0]
    selected_document_type_fake: DocumentType = main_context.all_seeder.document_type_seeder.document_type_fake.data[0]
    selected_account_fake: Account = main_context.all_seeder.document_seeder.document_fake.account_fake.data[0]
    selected_session_fake: Session = main_context.all_seeder.session_seeder.session_fake.data[0]
    document_patcher_body: CreateOneBody = CreateOneBody(
        name=f"patched.name{uuid.uuid4()}",
        description=f"patched.description{uuid.uuid4()}",
        document_type_id=selected_document_type_fake.id,
        account_id=selected_account_fake.id
    )
    headers: dict = {
        "Authorization": f"Bearer {selected_session_fake.access_token}"
    }
    response: Response = await main_context.client.patch(
        url=f"{url_path}/{selected_document_fake.id}",
        json=json.loads(document_patcher_body.json()),
        headers=headers
    )

    content: Content[Document] = Content[Document](
        **response.json(),
        status_code=response.status_code
    )
    assert content.status_code == status.HTTP_200_OK
    assert content.data.id == selected_document_fake.id
    assert content.data.name == document_patcher_body.name
    assert content.data.description == document_patcher_body.description
    assert content.data.document_type_id == document_patcher_body.document_type_id
    assert content.data.account_id == document_patcher_body.account_id


@pytest.mark.asyncio
async def test__delete_one_by_id__should_delete_one_document__succeed(main_context: MainContext):
    selected_document_fake: Document = main_context.all_seeder.document_seeder.document_fake.data[0]
    selected_session_fake: Session = main_context.all_seeder.session_seeder.session_fake.data[0]
    headers: dict = {
        "Authorization": f"Bearer {selected_session_fake.access_token}"
    }
    response: Response = await main_context.client.delete(
        url=f"{url_path}/{selected_document_fake.id}",
        headers=headers
    )

    content: Content[Document] = Content[Document](
        **response.json(),
        status_code=response.status_code
    )
    assert content.status_code == status.HTTP_200_OK
    assert content.data == selected_document_fake
    main_context.all_seeder.delete_many_document_by_id_cascade(selected_document_fake.id)
