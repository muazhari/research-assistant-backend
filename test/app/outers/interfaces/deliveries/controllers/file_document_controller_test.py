import hashlib
import json
import pathlib
import uuid

import pytest as pytest
from httpx import Response

from app.inners.models.daos.document import Document
from app.inners.models.daos.file_document import FileDocument
from app.inners.models.daos.session import Session
from app.inners.models.dtos.contracts.content import Content
from app.inners.models.dtos.contracts.requests.managements.file_documents.create_one_body import \
    CreateOneBody
from app.inners.models.dtos.contracts.requests.managements.file_documents.patch_one_body import \
    PatchOneBody
from app.inners.models.dtos.contracts.responses.managements.documents.file_document_response import FileDocumentResponse
from test.conftest import MainTest

url_path: str = "/api/documents/files"


@pytest.mark.asyncio
async def test__find_one_by_id__should__succeed(main_test: MainTest):
    selected_document_mock: Document = main_test.all_seeder.document_seeder.document_mock.data[0]
    selected_file_document_mock: FileDocument = main_test.all_seeder.file_document_seeder.file_document_mock.data[0]
    selected_session_mock: Session = main_test.all_seeder.session_seeder.session_mock.data[0]
    headers: dict = {
        "Authorization": f"Bearer {selected_session_mock.access_token}"
    }
    response: Response = await main_test.client.get(
        url=f"{url_path}/{selected_file_document_mock.id}",
        headers=headers
    )

    assert response.status_code == 200
    response_body: Content[FileDocumentResponse] = Content[FileDocumentResponse](**response.json())
    assert response_body.data.id == selected_file_document_mock.id
    assert response_body.data.document_name == selected_document_mock.name
    assert response_body.data.document_description == selected_document_mock.description
    assert response_body.data.document_type_id == selected_document_mock.document_type_id
    assert response_body.data.document_account_id == selected_document_mock.account_id
    assert response_body.data.file_name == selected_file_document_mock.file_name
    assert response_body.data.file_data_hash == selected_file_document_mock.file_data_hash
    assert response_body.data.file_meta == dict()


@pytest.mark.asyncio
async def test__create_one__should_create_one_file_document__succeed(main_test: MainTest):
    selected_session_mock: Session = main_test.all_seeder.session_seeder.session_mock.data[0]
    selected_document_mock: Document = main_test.all_seeder.document_seeder.document_mock.data[0]
    selected_file_document_data_mock: bytes = main_test.all_seeder.file_document_seeder.file_document_mock.file_data[0]
    selected_file_document_mock: FileDocument = main_test.all_seeder.file_document_seeder.file_document_mock.data[0]
    file_document_creator_body: CreateOneBody = CreateOneBody(
        document_name=f"name{uuid.uuid4()}",
        document_description=f"description{uuid.uuid4()}",
        document_type_id=selected_document_mock.document_type_id,
        document_account_id=selected_document_mock.account_id,
        file_name=f"file_name{uuid.uuid4()}{pathlib.Path(selected_file_document_mock.file_name).suffix}",
    )
    headers: dict = {
        "Authorization": f"Bearer {selected_session_mock.access_token}"
    }
    response: Response = await main_test.client.post(
        url=url_path,
        json=json.loads(file_document_creator_body.json()),
        headers=headers,
        files={"file_data": selected_file_document_data_mock}
    )

    assert response.status_code == 201
    response_body: Content[FileDocumentResponse] = Content[FileDocumentResponse](**response.json())
    assert response_body.data.document_name == file_document_creator_body.document_name
    assert response_body.data.document_description == file_document_creator_body.document_description
    assert response_body.data.document_type_id == file_document_creator_body.document_type_id
    assert response_body.data.document_account_id == file_document_creator_body.document_account_id
    assert response_body.data.file_name == file_document_creator_body.file_name
    assert response_body.data.file_data_hash == hashlib.sha256(selected_file_document_data_mock).hexdigest()
    assert response_body.data.file_meta == dict()


@pytest.mark.asyncio
async def test__patch_one_by_id__should_patch_one_file_document__succeed(main_test: MainTest):
    selected_session_mock: Session = main_test.all_seeder.session_seeder.session_mock.data[0]
    selected_file_document_mock: FileDocument = main_test.all_seeder.file_document_seeder.file_document_mock.data[0]
    selected_file_document_data_mock: bytes = main_test.all_seeder.file_document_seeder.file_document_mock.file_data[0]
    selected_document_mock: Document = main_test.all_seeder.document_seeder.document_mock.data[0]
    file_document_patcher_body: PatchOneBody = PatchOneBody(
        document_name=f"patched.name{uuid.uuid4()}",
        document_description=f"patched.description{uuid.uuid4()}",
        document_type_id=selected_document_mock.document_type_id,
        document_account_id=selected_document_mock.account_id,
        file_name=f"patched.file_name{uuid.uuid4()}{pathlib.Path(selected_file_document_mock.file_name).suffix}"
    )
    headers: dict = {
        "Authorization": f"Bearer {selected_session_mock.access_token}"
    }
    response: Response = await main_test.client.patch(
        url=f"{url_path}/{selected_file_document_mock.id}",
        json=json.loads(file_document_patcher_body.json()),
        headers=headers,
        files={"file_data": selected_file_document_data_mock}
    )

    assert response.status_code == 200
    response_body: Content[FileDocumentResponse] = Content[FileDocumentResponse](**response.json())
    assert response_body.data.document_name == file_document_patcher_body.document_name
    assert response_body.data.document_description == file_document_patcher_body.document_description
    assert response_body.data.document_type_id == file_document_patcher_body.document_type_id
    assert response_body.data.document_account_id == file_document_patcher_body.document_account_id
    assert response_body.data.file_name == file_document_patcher_body.file_name
    assert response_body.data.file_data_hash == hashlib.sha256(selected_file_document_data_mock).hexdigest()
    assert response_body.data.file_meta == dict()


@pytest.mark.asyncio
async def test__delete_one_by_id__should_delete_one_file_document__succeed(main_test: MainTest):
    selected_document_mock: Document = main_test.all_seeder.document_seeder.document_mock.data[0]
    selected_file_document_mock: FileDocument = main_test.all_seeder.file_document_seeder.file_document_mock.data[0]
    selected_session_mock: Session = main_test.all_seeder.session_seeder.session_mock.data[0]
    headers: dict = {
        "Authorization": f"Bearer {selected_session_mock.access_token}"
    }
    response: Response = await main_test.client.delete(
        url=f"{url_path}/{selected_file_document_mock.id}",
        headers=headers
    )

    assert response.status_code == 200
    response_body: Content[FileDocumentResponse] = Content[FileDocumentResponse](**response.json())
    assert response_body.data.id == selected_file_document_mock.id
    assert response_body.data.document_name == selected_document_mock.name
    assert response_body.data.document_description == selected_document_mock.description
    assert response_body.data.document_type_id == selected_document_mock.document_type_id
    assert response_body.data.document_account_id == selected_document_mock.account_id
    assert response_body.data.file_name == selected_file_document_mock.file_name
    assert response_body.data.file_data_hash == selected_file_document_mock.file_data_hash
    assert response_body.data.file_meta == dict()
    main_test.all_seeder.delete_many_file_document_by_id_cascade(selected_file_document_mock.id)
