import hashlib
import json
import uuid

import pytest as pytest
from httpx import Response
from starlette import status

from apps.inners.models.daos.account import Account
from apps.inners.models.daos.document import Document
from apps.inners.models.daos.document_type import DocumentType
from apps.inners.models.daos.session import Session
from apps.inners.models.daos.text_document import TextDocument
from apps.inners.models.dtos.content import Content
from apps.inners.models.dtos.contracts.requests.managements.text_documents.create_one_body import \
    CreateOneBody
from apps.inners.models.dtos.contracts.requests.managements.text_documents.patch_one_body import \
    PatchOneBody
from apps.inners.models.dtos.contracts.responses.managements.documents.text_document_response import \
    TextDocumentResponse
from tests.main_context import MainContext

url_path: str = "/api/documents/texts"


@pytest.mark.asyncio
async def test__find_one_by_id__should__succeed(main_context: MainContext):
    selected_document_mock: Document = main_context.all_seeder.document_seeder.document_mock.data[1]
    selected_text_document_mock: TextDocument = main_context.all_seeder.text_document_seeder.text_document_mock.data[0]
    selected_session_mock: Session = main_context.all_seeder.session_seeder.session_mock.data[0]
    headers: dict = {
        "Authorization": f"Bearer {selected_session_mock.access_token}"
    }
    response: Response = await main_context.client.get(
        url=f"{url_path}/{selected_text_document_mock.id}",
        headers=headers
    )

    content: Content[TextDocumentResponse] = Content[TextDocumentResponse](
        **response.json(),
        status_code=response.status_code
    )
    assert content.status_code == status.HTTP_200_OK
    assert content.data.id == selected_text_document_mock.id
    assert content.data.document_name == selected_document_mock.name
    assert content.data.document_description == selected_document_mock.description
    assert content.data.document_type_id == selected_document_mock.document_type_id
    assert content.data.document_account_id == selected_document_mock.account_id
    assert content.data.text_content == selected_text_document_mock.text_content
    assert content.data.text_content_hash == selected_text_document_mock.text_content_hash


@pytest.mark.asyncio
async def test__create_one__should_create_one_text_document__succeed(main_context: MainContext):
    selected_session_mock: Session = main_context.all_seeder.session_seeder.session_mock.data[0]
    selected_document_mock: Document = main_context.all_seeder.document_seeder.document_mock.data[1]
    selected_document_type_mock: DocumentType = main_context.all_seeder.document_type_seeder.document_type_mock.data[0]
    selected_account_mock: Account = main_context.all_seeder.document_seeder.document_mock.account_mock.data[0]
    selected_text_document_mock: TextDocument = main_context.all_seeder.text_document_seeder.text_document_mock.data[0]
    text_document_creator_body: CreateOneBody = CreateOneBody(
        name=f"name{uuid.uuid4()}",
        description=f"description{uuid.uuid4()}",
        document_id=selected_document_mock.id,
        document_type_id=selected_document_type_mock.id,
        account_id=selected_account_mock.id,
        text_content=selected_text_document_mock.text_content,
        text_content_hash=selected_text_document_mock.text_content_hash
    )
    headers: dict = {
        "Authorization": f"Bearer {selected_session_mock.access_token}"
    }
    response: Response = await main_context.client.post(
        url=url_path,
        json=json.loads(text_document_creator_body.json()),
        headers=headers
    )

    content: Content[TextDocumentResponse] = Content[TextDocumentResponse](
        **response.json(),
        status_code=response.status_code
    )
    assert content.status_code == status.HTTP_201_CREATED
    assert content.data.document_name == text_document_creator_body.name
    assert content.data.document_description == text_document_creator_body.description
    assert content.data.document_type_id == text_document_creator_body.document_type_id
    assert content.data.document_account_id == text_document_creator_body.account_id
    assert content.data.text_content == text_document_creator_body.text_content
    assert content.data.text_content_hash == text_document_creator_body.text_content_hash


@pytest.mark.asyncio
async def test__patch_one_by_id__should_patch_one_text_document__succeed(main_context: MainContext):
    selected_session_mock: Session = main_context.all_seeder.session_seeder.session_mock.data[0]
    selected_document_mock: Document = main_context.all_seeder.document_seeder.document_mock.data[1]
    selected_text_document_mock: TextDocument = main_context.all_seeder.text_document_seeder.text_document_mock.data[0]
    selected_document_type_mock: DocumentType = main_context.all_seeder.document_type_seeder.document_type_mock.data[0]
    selected_account_mock: Account = main_context.all_seeder.document_seeder.document_mock.account_mock.data[0]
    text_document_patcher_body: PatchOneBody = PatchOneBody(
        name=f"patched.name{uuid.uuid4()}",
        description=f"patched.description{uuid.uuid4()}",
        document_id=selected_document_mock.id,
        document_type_id=selected_document_type_mock.id,
        account_id=selected_account_mock.id,
        text_content=selected_text_document_mock.text_content,
    )
    headers: dict = {
        "Authorization": f"Bearer {selected_session_mock.access_token}"
    }
    response: Response = await main_context.client.patch(
        url=f"{url_path}/{selected_text_document_mock.id}",
        json=json.loads(text_document_patcher_body.json()),
        headers=headers
    )

    content: Content[TextDocumentResponse] = Content[TextDocumentResponse](
        **response.json(),
        status_code=response.status_code
    )
    assert content.status_code == status.HTTP_200_OK
    assert content.data.document_name == text_document_patcher_body.name
    assert content.data.document_description == text_document_patcher_body.description
    assert content.data.document_type_id == text_document_patcher_body.document_type_id
    assert content.data.document_account_id == text_document_patcher_body.account_id
    assert content.data.text_content == text_document_patcher_body.text_content
    assert content.data.text_content_hash == hashlib.sha256(
        text_document_patcher_body.text_content.encode()).hexdigest()


@pytest.mark.asyncio
async def test__delete_one_by_id__should_delete_one_text_document__succeed(main_context: MainContext):
    selected_document_mock: Document = main_context.all_seeder.document_seeder.document_mock.data[1]
    selected_text_document_mock: TextDocument = main_context.all_seeder.text_document_seeder.text_document_mock.data[0]
    selected_session_mock: Session = main_context.all_seeder.session_seeder.session_mock.data[0]
    headers: dict = {
        "Authorization": f"Bearer {selected_session_mock.access_token}"
    }
    response: Response = await main_context.client.delete(
        url=f"{url_path}/{selected_text_document_mock.id}",
        headers=headers
    )

    content: Content[TextDocumentResponse] = Content[TextDocumentResponse](
        **response.json(),
        status_code=response.status_code
    )
    assert content.status_code == status.HTTP_200_OK
    assert content.data.id == selected_text_document_mock.id
    assert content.data.document_name == selected_document_mock.name
    assert content.data.document_description == selected_document_mock.description
    assert content.data.document_type_id == selected_document_mock.document_type_id
    assert content.data.document_account_id == selected_document_mock.account_id
    assert content.data.text_content == selected_text_document_mock.text_content
    assert content.data.text_content_hash == selected_text_document_mock.text_content_hash
    main_context.all_seeder.delete_many_text_document_by_id_cascade(selected_text_document_mock.id)
