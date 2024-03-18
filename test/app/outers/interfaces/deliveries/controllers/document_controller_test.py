import json
import json
import uuid

import pytest as pytest
from httpx import Response

from app.inners.models.daos.account import Account
from app.inners.models.daos.document import Document
from app.inners.models.daos.document_type import DocumentType
from app.inners.models.daos.session import Session
from app.inners.models.dtos.contracts.content import Content
from app.inners.models.dtos.contracts.requests.managements.documents.create_one_body import \
    CreateOneBody
from test.conftest import MainTest

url_path: str = "/api/documents"


@pytest.mark.asyncio
async def test__find_one_by_id__should__succeed(main_test: MainTest):
    selected_document_mock: Document = main_test.all_seeder.document_seeder.document_mock.data[0]
    selected_session_mock: Session = main_test.all_seeder.session_seeder.session_mock.data[0]
    headers: dict = {
        "Authorization": f"Bearer {selected_session_mock.access_token}"
    }
    response: Response = await main_test.client.get(
        url=f"{url_path}/{selected_document_mock.id}",
        headers=headers
    )

    assert response.status_code == 200
    response_body: Content[Document] = Content[Document](**response.json())
    assert response_body.data == selected_document_mock


@pytest.mark.asyncio
async def test__create_one__should_create_one_document__succeed(main_test: MainTest):
    selected_document_type_mock: DocumentType = main_test.all_seeder.document_type_seeder.document_type_mock.data[0]
    selected_account_mock: Account = main_test.all_seeder.document_seeder.document_mock.account_mock.data[0]
    selected_session_mock: Session = main_test.all_seeder.session_seeder.session_mock.data[0]
    document_to_create_body: CreateOneBody = CreateOneBody(
        name=f"name{uuid.uuid4()}",
        description=f"description{uuid.uuid4()}",
        document_type_id=selected_document_type_mock.id,
        account_id=selected_account_mock.id
    )
    headers: dict = {
        "Authorization": f"Bearer {selected_session_mock.access_token}"
    }
    response: Response = await main_test.client.post(
        url=url_path,
        json=json.loads(document_to_create_body.json()),
        headers=headers
    )

    assert response.status_code == 201
    response_body: Content[Document] = Content[Document](**response.json())
    assert response_body.data.name == document_to_create_body.name
    assert response_body.data.description == document_to_create_body.description
    assert response_body.data.document_type_id == document_to_create_body.document_type_id
    assert response_body.data.account_id == document_to_create_body.account_id


@pytest.mark.asyncio
async def test__patch_one_by_id__should_patch_one_document__succeed(main_test: MainTest):
    selected_document_mock: Document = main_test.all_seeder.document_seeder.document_mock.data[0]
    selected_document_type_mock: DocumentType = main_test.all_seeder.document_type_seeder.document_type_mock.data[0]
    selected_account_mock: Account = main_test.all_seeder.document_seeder.document_mock.account_mock.data[0]
    selected_session_mock: Session = main_test.all_seeder.session_seeder.session_mock.data[0]
    document_to_patch_body: CreateOneBody = CreateOneBody(
        name=f"patched.name{uuid.uuid4()}",
        description=f"patched.description{uuid.uuid4()}",
        document_type_id=selected_document_type_mock.id,
        account_id=selected_account_mock.id
    )
    headers: dict = {
        "Authorization": f"Bearer {selected_session_mock.access_token}"
    }
    response: Response = await main_test.client.patch(
        url=f"{url_path}/{selected_document_mock.id}",
        json=json.loads(document_to_patch_body.json()),
        headers=headers
    )

    assert response.status_code == 200
    response_body: Content[Document] = Content[Document](**response.json())
    assert response_body.data.id == selected_document_mock.id
    assert response_body.data.name == document_to_patch_body.name
    assert response_body.data.description == document_to_patch_body.description
    assert response_body.data.document_type_id == document_to_patch_body.document_type_id
    assert response_body.data.account_id == document_to_patch_body.account_id


@pytest.mark.asyncio
async def test__delete_one_by_id__should_delete_one_document__succeed(main_test: MainTest):
    selected_document_mock: Document = main_test.all_seeder.document_seeder.document_mock.data[0]
    selected_session_mock: Session = main_test.all_seeder.session_seeder.session_mock.data[0]
    headers: dict = {
        "Authorization": f"Bearer {selected_session_mock.access_token}"
    }
    response: Response = await main_test.client.delete(
        url=f"{url_path}/{selected_document_mock.id}",
        headers=headers
    )

    assert response.status_code == 200
    response_body: Content[Document] = Content[Document](**response.json())
    assert response_body.data == selected_document_mock
    main_test.all_seeder.delete_many_document_by_id_cascade(selected_document_mock.id)
