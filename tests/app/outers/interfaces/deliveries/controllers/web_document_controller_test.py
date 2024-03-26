import hashlib
import hashlib
import json
import uuid

import pytest as pytest
from httpx import Response

from apps.inners.models.daos.account import Account
from apps.inners.models.daos.document import Document
from apps.inners.models.daos.document_type import DocumentType
from apps.inners.models.daos.session import Session
from apps.inners.models.daos.web_document import WebDocument
from apps.inners.models.dtos.contracts.content import Content
from apps.inners.models.dtos.contracts.requests.managements.web_documents.create_one_body import \
    CreateOneBody
from apps.inners.models.dtos.contracts.requests.managements.web_documents.patch_one_body import \
    PatchOneBody
from apps.inners.models.dtos.contracts.responses.managements.documents.web_document_response import WebDocumentResponse
from tests.conftest import MainTest

url_path: str = "/api/documents/webs"


@pytest.mark.asyncio
async def test__find_one_by_id__should__succeed(main_test: MainTest):
    selected_document_mock: Document = main_test.all_seeder.document_seeder.document_mock.data[2]
    selected_web_document_mock: WebDocument = main_test.all_seeder.web_document_seeder.web_document_mock.data[0]
    selected_session_mock: Session = main_test.all_seeder.session_seeder.session_mock.data[0]
    headers: dict = {
        "Authorization": f"Bearer {selected_session_mock.access_token}"
    }
    response: Response = await main_test.client.get(
        url=f"{url_path}/{selected_web_document_mock.id}",
        headers=headers
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
async def test__create_one__should_create_one_web_document__succeed(main_test: MainTest):
    selected_session_mock: Session = main_test.all_seeder.session_seeder.session_mock.data[0]
    selected_document_mock: Document = main_test.all_seeder.document_seeder.document_mock.data[2]
    selected_document_type_mock: DocumentType = main_test.all_seeder.document_type_seeder.document_type_mock.data[0]
    selected_account_mock: Account = main_test.all_seeder.document_seeder.document_mock.account_mock.data[0]
    selected_web_document_mock: WebDocument = main_test.all_seeder.web_document_seeder.web_document_mock.data[0]
    web_document_creator_body: CreateOneBody = CreateOneBody(
        name=f"name{uuid.uuid4()}",
        description=f"description{uuid.uuid4()}",
        document_id=selected_document_mock.id,
        document_type_id=selected_document_type_mock.id,
        account_id=selected_account_mock.id,
        web_url=selected_web_document_mock.web_url,
        web_url_hash=selected_web_document_mock.web_url_hash
    )
    selected_session_mock: Session = main_test.all_seeder.session_seeder.session_mock.data[0]
    headers: dict = {
        "Authorization": f"Bearer {selected_session_mock.access_token}"
    }
    response: Response = await main_test.client.post(
        url=url_path,
        json=json.loads(web_document_creator_body.json()),
        headers=headers
    )

    assert response.status_code == 201
    response_body: Content[WebDocumentResponse] = Content[WebDocumentResponse](**response.json())
    assert response_body.data.document_name == web_document_creator_body.name
    assert response_body.data.document_description == web_document_creator_body.description
    assert response_body.data.document_type_id == web_document_creator_body.document_type_id
    assert response_body.data.document_account_id == web_document_creator_body.account_id
    assert response_body.data.web_url == web_document_creator_body.web_url
    assert response_body.data.web_url_hash == hashlib.sha256(web_document_creator_body.web_url.encode()).hexdigest()


@pytest.mark.asyncio
async def test__patch_one_by_id__should_patch_one_web_document__succeed(main_test: MainTest):
    selected_session_mock: Session = main_test.all_seeder.session_seeder.session_mock.data[0]
    selected_document_mock: Document = main_test.all_seeder.document_seeder.document_mock.data[2]
    selected_web_document_mock: WebDocument = main_test.all_seeder.web_document_seeder.web_document_mock.data[0]
    selected_document_type_mock: DocumentType = main_test.all_seeder.document_type_seeder.document_type_mock.data[0]
    selected_account_mock: Account = main_test.all_seeder.document_seeder.document_mock.account_mock.data[0]
    web_document_patcher_body: PatchOneBody = PatchOneBody(
        name=f"patched.name{uuid.uuid4()}",
        description=f"patched.description{uuid.uuid4()}",
        document_id=selected_document_mock.id,
        document_type_id=selected_document_type_mock.id,
        account_id=selected_account_mock.id,
        web_url=selected_web_document_mock.web_url,
        web_url_hash=selected_web_document_mock.web_url_hash
    )
    headers: dict = {
        "Authorization": f"Bearer {selected_session_mock.access_token}"
    }
    response: Response = await main_test.client.patch(
        url=f"{url_path}/{selected_web_document_mock.id}",
        json=json.loads(web_document_patcher_body.json()),
        headers=headers
    )

    assert response.status_code == 200
    response_body: Content[WebDocumentResponse] = Content[WebDocumentResponse](**response.json())
    assert response_body.data.document_name == web_document_patcher_body.name
    assert response_body.data.document_description == web_document_patcher_body.description
    assert response_body.data.document_type_id == web_document_patcher_body.document_type_id
    assert response_body.data.document_account_id == web_document_patcher_body.account_id
    assert response_body.data.web_url == web_document_patcher_body.web_url
    assert response_body.data.web_url_hash == hashlib.sha256(web_document_patcher_body.web_url.encode()).hexdigest()


@pytest.mark.asyncio
async def test__delete_one_by_id__should_delete_one_web_document__succeed(main_test: MainTest):
    selected_document_mock: Document = main_test.all_seeder.document_seeder.document_mock.data[2]
    selected_web_document_mock: WebDocument = main_test.all_seeder.web_document_seeder.web_document_mock.data[0]
    selected_session_mock: Session = main_test.all_seeder.session_seeder.session_mock.data[0]
    headers: dict = {
        "Authorization": f"Bearer {selected_session_mock.access_token}"
    }
    response: Response = await main_test.client.delete(
        url=f"{url_path}/{selected_web_document_mock.id}",
        headers=headers
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
    main_test.all_seeder.delete_many_web_document_by_id_cascade(selected_web_document_mock.id)
