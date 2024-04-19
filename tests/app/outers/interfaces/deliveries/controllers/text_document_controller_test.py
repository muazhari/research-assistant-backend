import hashlib
import uuid
from typing import Dict, Any, List

import pytest as pytest
from httpx import Response
from starlette import status

from apps.inners.models.daos.account import Account
from apps.inners.models.daos.document import Document
from apps.inners.models.daos.session import Session
from apps.inners.models.daos.text_document import TextDocument
from apps.inners.models.dtos.constants.document_type_constant import DocumentTypeConstant
from apps.inners.models.dtos.content import Content
from apps.inners.models.dtos.contracts.requests.managements.text_documents.create_one_body import \
    CreateOneBody
from apps.inners.models.dtos.contracts.requests.managements.text_documents.patch_one_body import \
    PatchOneBody
from apps.inners.models.dtos.contracts.responses.managements.documents.text_document_response import \
    TextDocumentResponse
from tests.main_context import MainContext

url_path: str = "/api/document-texts"


@pytest.mark.asyncio
async def test__find_many_with_pagination__should__succeed(main_context: MainContext):
    selected_session_fake: Session = main_context.all_seeder.session_seeder.session_fake.data[0]
    selected_text_document_fakes: List[TextDocument] = []
    selected_document_fakes: List[Document] = []
    for text_document_fake in main_context.all_seeder.text_document_seeder.text_document_fake.data:
        for document_fake in main_context.all_seeder.document_seeder.document_fake.data:
            if text_document_fake.id == document_fake.id:
                selected_document_fakes.append(document_fake)
                if document_fake.account_id == selected_session_fake.account_id:
                    selected_text_document_fakes.append(text_document_fake)

    headers: Dict[str, Any] = {
        "Authorization": f"Bearer {selected_session_fake.access_token}"
    }
    params: Dict[str, Any] = {
        "page_position": 1,
        "page_size": len(selected_text_document_fakes)
    }
    response: Response = await main_context.client.get(
        url=url_path,
        headers=headers,
        params=params
    )

    content: Content[List[TextDocumentResponse]] = Content[List[TextDocumentResponse]](
        **response.json(),
        status_code=response.status_code
    )
    assert content.status_code == status.HTTP_200_OK
    assert len(content.data) == len(selected_text_document_fakes)
    for text_document_response in content.data:
        for selected_document_fake in selected_document_fakes:
            for selected_text_document_fake in selected_text_document_fakes:
                if text_document_response.id == selected_document_fake.id == selected_text_document_fake.id:
                    assert text_document_response.name == selected_document_fake.name
                    assert text_document_response.description == selected_document_fake.description
                    assert text_document_response.document_type_id == selected_document_fake.document_type_id
                    assert text_document_response.account_id == selected_document_fake.account_id
                    assert text_document_response.text_content == selected_text_document_fake.text_content
                    assert text_document_response.text_content_hash == selected_text_document_fake.text_content_hash


@pytest.mark.asyncio
async def test__find_one_by_id__should__succeed(main_context: MainContext):
    selected_document_fake: Document = main_context.all_seeder.document_seeder.document_fake.data[1]
    selected_text_document_fake: TextDocument = main_context.all_seeder.text_document_seeder.text_document_fake.data[0]
    selected_session_fake: Session = main_context.all_seeder.session_seeder.session_fake.data[0]
    headers: Dict[str, Any] = {
        "Authorization": f"Bearer {selected_session_fake.access_token}"
    }
    response: Response = await main_context.client.get(
        url=f"{url_path}/{selected_text_document_fake.id}",
        headers=headers
    )

    content: Content[TextDocumentResponse] = Content[TextDocumentResponse](
        **response.json(),
        status_code=response.status_code
    )
    assert content.status_code == status.HTTP_200_OK
    assert content.data.id == selected_text_document_fake.id
    assert content.data.name == selected_document_fake.name
    assert content.data.description == selected_document_fake.description
    assert content.data.document_type_id == DocumentTypeConstant.TEXT
    assert content.data.account_id == selected_document_fake.account_id
    assert content.data.text_content == selected_text_document_fake.text_content
    assert content.data.text_content_hash == selected_text_document_fake.text_content_hash


@pytest.mark.asyncio
async def test__create_one__should_create_one_text_document__succeed(main_context: MainContext):
    selected_session_fake: Session = main_context.all_seeder.session_seeder.session_fake.data[0]
    selected_account_fake: Account = main_context.all_seeder.document_seeder.document_fake.account_fake.data[0]
    selected_text_document_fake: TextDocument = main_context.all_seeder.text_document_seeder.text_document_fake.data[0]
    text_document_creator_body: CreateOneBody = CreateOneBody(
        name=f"name{uuid.uuid4()}",
        description=f"description{uuid.uuid4()}",
        account_id=selected_account_fake.id,
        text_content=selected_text_document_fake.text_content,
    )
    headers: Dict[str, Any] = {
        "Authorization": f"Bearer {selected_session_fake.access_token}"
    }
    response: Response = await main_context.client.post(
        url=url_path,
        json=text_document_creator_body.model_dump(mode="json"),
        headers=headers
    )

    content: Content[TextDocumentResponse] = Content[TextDocumentResponse](
        **response.json(),
        status_code=response.status_code
    )
    assert content.status_code == status.HTTP_201_CREATED
    assert content.data.name == text_document_creator_body.name
    assert content.data.description == text_document_creator_body.description
    assert content.data.document_type_id == DocumentTypeConstant.TEXT
    assert content.data.account_id == text_document_creator_body.account_id
    assert content.data.text_content == text_document_creator_body.text_content
    assert content.data.text_content_hash == hashlib.sha256(
        text_document_creator_body.text_content.encode()
    ).hexdigest()

    text_document: TextDocument = TextDocument(
        id=content.data.id,
        text_content=content.data.text_content,
        text_content_hash=content.data.text_content_hash
    )
    main_context.all_seeder.text_document_seeder.text_document_fake.data.append(text_document)


@pytest.mark.asyncio
async def test__patch_one_by_id__should_patch_one_text_document__succeed(main_context: MainContext):
    selected_session_fake: Session = main_context.all_seeder.session_seeder.session_fake.data[0]
    selected_text_document_fake: TextDocument = main_context.all_seeder.text_document_seeder.text_document_fake.data[0]
    selected_account_fake: Account = main_context.all_seeder.document_seeder.document_fake.account_fake.data[0]
    text_document_patcher_body: PatchOneBody = PatchOneBody(
        name=f"patched.name{uuid.uuid4()}",
        description=f"patched.description{uuid.uuid4()}",
        account_id=selected_account_fake.id,
        text_content=selected_text_document_fake.text_content,
    )
    headers: Dict[str, Any] = {
        "Authorization": f"Bearer {selected_session_fake.access_token}"
    }
    response: Response = await main_context.client.patch(
        url=f"{url_path}/{selected_text_document_fake.id}",
        json=text_document_patcher_body.model_dump(mode="json"),
        headers=headers
    )

    content: Content[TextDocumentResponse] = Content[TextDocumentResponse](
        **response.json(),
        status_code=response.status_code
    )
    assert content.status_code == status.HTTP_200_OK
    assert content.data.name == text_document_patcher_body.name
    assert content.data.description == text_document_patcher_body.description
    assert content.data.document_type_id == DocumentTypeConstant.TEXT
    assert content.data.account_id == text_document_patcher_body.account_id
    assert content.data.text_content == text_document_patcher_body.text_content
    assert content.data.text_content_hash == hashlib.sha256(
        text_document_patcher_body.text_content.encode()
    ).hexdigest()


@pytest.mark.asyncio
async def test__delete_one_by_id__should_delete_one_text_document__succeed(main_context: MainContext):
    selected_document_fake: Document = main_context.all_seeder.document_seeder.document_fake.data[1]
    selected_text_document_fake: TextDocument = main_context.all_seeder.text_document_seeder.text_document_fake.data[0]
    selected_session_fake: Session = main_context.all_seeder.session_seeder.session_fake.data[0]
    headers: Dict[str, Any] = {
        "Authorization": f"Bearer {selected_session_fake.access_token}"
    }
    response: Response = await main_context.client.delete(
        url=f"{url_path}/{selected_text_document_fake.id}",
        headers=headers
    )

    content: Content[TextDocumentResponse] = Content[TextDocumentResponse](
        **response.json(),
        status_code=response.status_code
    )
    assert content.status_code == status.HTTP_200_OK
    assert content.data.id == selected_text_document_fake.id
    assert content.data.name == selected_document_fake.name
    assert content.data.description == selected_document_fake.description
    assert content.data.document_type_id == DocumentTypeConstant.TEXT
    assert content.data.account_id == selected_document_fake.account_id
    assert content.data.text_content == selected_text_document_fake.text_content
    assert content.data.text_content_hash == selected_text_document_fake.text_content_hash
    main_context.all_seeder.delete_many_text_document_by_id_cascade(selected_text_document_fake.id)
