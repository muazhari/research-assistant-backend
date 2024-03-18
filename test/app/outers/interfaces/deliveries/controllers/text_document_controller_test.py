import hashlib
import hashlib
import json
import uuid

import pytest as pytest
from httpx import Response

from app.inners.models.daos.account import Account
from app.inners.models.daos.document import Document
from app.inners.models.daos.document_type import DocumentType
from app.inners.models.daos.text_document import TextDocument
from app.inners.models.dtos.contracts.content import Content
from app.inners.models.dtos.contracts.requests.managements.text_documents.create_one_body import \
    CreateOneBody
from app.inners.models.dtos.contracts.requests.managements.text_documents.patch_one_body import \
    PatchOneBody
from app.inners.models.dtos.contracts.responses.managements.documents.text_document_response import TextDocumentResponse
from test.conftest import MainTest

url_path: str = "/api/documents/texts"


@pytest.mark.asyncio
async def test__find_one_by_id__should__succeed(main_test: MainTest):
    selected_document_mock: Document = main_test.all_seeder.document_seeder.document_mock.data[1]
    selected_text_document_mock: TextDocument = main_test.all_seeder.text_document_seeder.text_document_mock.data[0]
    response: Response = await main_test.client.get(
        url=f"{url_path}/{selected_text_document_mock.id}"
    )
    assert response.status_code == 200
    response_body: Content[TextDocumentResponse] = Content[TextDocumentResponse](**response.json())
    assert response_body.data.id == selected_text_document_mock.id
    assert response_body.data.document_name == selected_document_mock.name
    assert response_body.data.document_description == selected_document_mock.description
    assert response_body.data.document_type_id == selected_document_mock.document_type_id
    assert response_body.data.document_account_id == selected_document_mock.account_id
    assert response_body.data.text_content == selected_text_document_mock.text_content
    assert response_body.data.text_content_hash == selected_text_document_mock.text_content_hash


@pytest.mark.asyncio
async def test__create_one__should_create_one_text_document__succeed(main_test: MainTest):
    selected_document_mock: Document = main_test.all_seeder.document_seeder.document_mock.data[1]
    selected_document_type_mock: DocumentType = main_test.all_seeder.document_type_seeder.document_type_mock.data[0]
    selected_account_mock: Account = main_test.all_seeder.document_seeder.document_mock.account_mock.data[0]
    selected_text_document_mock: TextDocument = main_test.all_seeder.text_document_seeder.text_document_mock.data[0]
    text_document_to_create_body: CreateOneBody = CreateOneBody(
        name=f"name{uuid.uuid4()}",
        description=f"description{uuid.uuid4()}",
        document_id=selected_document_mock.id,
        document_type_id=selected_document_type_mock.id,
        account_id=selected_account_mock.id,
        text_content=selected_text_document_mock.text_content,
        text_content_hash=selected_text_document_mock.text_content_hash
    )
    response: Response = await main_test.client.post(
        url=url_path,
        json=json.loads(text_document_to_create_body.json())
    )
    assert response.status_code == 201
    response_body: Content[TextDocumentResponse] = Content[TextDocumentResponse](**response.json())
    assert response_body.data.document_name == text_document_to_create_body.name
    assert response_body.data.document_description == text_document_to_create_body.description
    assert response_body.data.document_type_id == text_document_to_create_body.document_type_id
    assert response_body.data.document_account_id == text_document_to_create_body.account_id
    assert response_body.data.text_content == text_document_to_create_body.text_content
    assert response_body.data.text_content_hash == text_document_to_create_body.text_content_hash


@pytest.mark.asyncio
async def test__patch_one_by_id__should_patch_one_text_document__succeed(main_test: MainTest):
    selected_text_document_mock: TextDocument = main_test.all_seeder.text_document_seeder.text_document_mock.data[1]
    selected_document_mock: Document = main_test.all_seeder.document_seeder.document_mock.data[0]
    selected_document_type_mock: DocumentType = main_test.all_seeder.document_type_seeder.document_type_mock.data[0]
    selected_account_mock: Account = main_test.all_seeder.document_seeder.document_mock.account_mock.data[0]
    text_document_to_patch_body: PatchOneBody = PatchOneBody(
        name=f"patched.name{uuid.uuid4()}",
        description=f"patched.description{uuid.uuid4()}",
        document_id=selected_document_mock.id,
        document_type_id=selected_document_type_mock.id,
        account_id=selected_account_mock.id,
        text_content=selected_text_document_mock.text_content,
    )
    response: Response = await main_test.client.patch(
        url=f"{url_path}/{selected_text_document_mock.id}",
        json=json.loads(text_document_to_patch_body.json())
    )
    assert response.status_code == 200
    response_body: Content[TextDocumentResponse] = Content[TextDocumentResponse](**response.json())
    assert response_body.data.document_name == text_document_to_patch_body.name
    assert response_body.data.document_description == text_document_to_patch_body.description
    assert response_body.data.document_type_id == text_document_to_patch_body.document_type_id
    assert response_body.data.document_account_id == text_document_to_patch_body.account_id
    assert response_body.data.text_content == text_document_to_patch_body.text_content
    assert response_body.data.text_content_hash == hashlib.sha256(
        text_document_to_patch_body.text_content.encode()).hexdigest()


@pytest.mark.asyncio
async def test__delete_one_by_id__should_delete_one_text_document__succeed(main_test: MainTest):
    selected_document_mock: Document = main_test.all_seeder.document_seeder.document_mock.data[1]
    selected_text_document_mock: TextDocument = main_test.all_seeder.text_document_seeder.text_document_mock.data[0]
    response: Response = await main_test.client.delete(
        url=f"{url_path}/{selected_text_document_mock.id}"
    )
    assert response.status_code == 200
    response_body: Content[TextDocumentResponse] = Content[TextDocumentResponse](**response.json())
    assert response_body.data.id == selected_text_document_mock.id
    assert response_body.data.document_name == selected_document_mock.name
    assert response_body.data.document_description == selected_document_mock.description
    assert response_body.data.document_type_id == selected_document_mock.document_type_id
    assert response_body.data.document_account_id == selected_document_mock.account_id
    assert response_body.data.text_content == selected_text_document_mock.text_content
    assert response_body.data.text_content_hash == selected_text_document_mock.text_content_hash
    main_test.all_seeder.delete_many_text_document_by_id_cascade(selected_text_document_mock.id)
