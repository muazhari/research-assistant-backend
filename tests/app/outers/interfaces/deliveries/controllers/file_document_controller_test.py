import hashlib
import pathlib
import uuid
from typing import Dict, Any, List

import pytest as pytest
from httpx import Response
from starlette import status

from apps.inners.models.daos.document import Document
from apps.inners.models.daos.file_document import FileDocument
from apps.inners.models.daos.session import Session
from apps.inners.models.dtos.constants.document_type_constant import DocumentTypeConstant
from apps.inners.models.dtos.content import Content
from apps.inners.models.dtos.contracts.requests.managements.file_documents.create_one_body import \
    CreateOneBody
from apps.inners.models.dtos.contracts.requests.managements.file_documents.patch_one_body import \
    PatchOneBody
from apps.inners.models.dtos.contracts.responses.managements.documents.file_document_response import \
    FileDocumentResponse
from tests.main_context import MainContext

url_path: str = "/api/document-files"


@pytest.mark.asyncio
async def test__find_many_with_pagination__should__succeed(main_context: MainContext):
    selected_session_fake: Session = main_context.all_seeder.session_seeder.session_fake.data[0]
    selected_file_document_fakes: List[FileDocument] = []
    selected_document_fakes: List[Document] = []
    for file_document_fake in main_context.all_seeder.file_document_seeder.file_document_fake.data:
        for document_fake in main_context.all_seeder.document_seeder.document_fake.data:
            if file_document_fake.id == document_fake.id:
                selected_document_fakes.append(document_fake)
                if document_fake.account_id == selected_session_fake.account_id:
                    selected_file_document_fakes.append(file_document_fake)

    headers: Dict[str, Any] = {
        "Authorization": f"Bearer {selected_session_fake.access_token}"
    }
    params: Dict[str, Any] = {
        "page_position": 1,
        "page_size": len(selected_file_document_fakes)
    }
    response: Response = await main_context.client.get(
        url=url_path,
        headers=headers,
        params=params
    )

    content: Content[List[FileDocumentResponse]] = Content[List[FileDocumentResponse]](
        **response.json(),
        status_code=response.status_code
    )
    assert content.status_code == status.HTTP_200_OK
    assert len(content.data) == len(selected_file_document_fakes)
    for file_document_response in content.data:
        for selected_document_fake in selected_document_fakes:
            for selected_file_document_fake in selected_file_document_fakes:
                if file_document_response.id == selected_document_fake.id == selected_file_document_fake.id:
                    assert file_document_response.name == selected_document_fake.name
                    assert file_document_response.description == selected_document_fake.description
                    assert file_document_response.document_type_id == selected_document_fake.document_type_id
                    assert file_document_response.account_id == selected_document_fake.account_id
                    assert file_document_response.file_name == selected_file_document_fake.file_name
                    assert file_document_response.file_data_hash == selected_file_document_fake.file_data_hash
                    assert file_document_response.file_metadata is not None


@pytest.mark.asyncio
async def test__find_one_by_id__should__succeed(main_context: MainContext):
    selected_document_fake: Document = main_context.all_seeder.document_seeder.document_fake.data[0]
    selected_file_document_fake: FileDocument = main_context.all_seeder.file_document_seeder.file_document_fake.data[0]
    selected_session_fake: Session = main_context.all_seeder.session_seeder.session_fake.data[0]
    headers: Dict[str, Any] = {
        "Authorization": f"Bearer {selected_session_fake.access_token}"
    }
    response: Response = await main_context.client.get(
        url=f"{url_path}/{selected_file_document_fake.id}",
        headers=headers
    )

    content: Content[FileDocumentResponse] = Content[FileDocumentResponse](
        **response.json(),
        status_code=response.status_code
    )
    assert content.status_code == status.HTTP_200_OK
    assert content.data.id == selected_file_document_fake.id
    assert content.data.name == selected_document_fake.name
    assert content.data.description == selected_document_fake.description
    assert content.data.document_type_id == DocumentTypeConstant.FILE
    assert content.data.account_id == selected_document_fake.account_id
    assert content.data.file_name == selected_file_document_fake.file_name
    assert content.data.file_data_hash == selected_file_document_fake.file_data_hash
    assert content.data.file_metadata is not None


@pytest.mark.asyncio
async def test__create_one__should_create_one_file_document__succeed(main_context: MainContext):
    selected_session_fake: Session = main_context.all_seeder.session_seeder.session_fake.data[0]
    selected_document_fake: Document = main_context.all_seeder.document_seeder.document_fake.data[0]
    selected_file_document_data_fake: bytes = main_context.all_seeder.file_document_seeder.file_document_fake.file_data[
        0]
    selected_file_document_fake: FileDocument = main_context.all_seeder.file_document_seeder.file_document_fake.data[0]
    file_document_creator_body: CreateOneBody = CreateOneBody(
        name=f"name{uuid.uuid4()}",
        description=f"description{uuid.uuid4()}",
        account_id=selected_document_fake.account_id,
        file_name=f"file_name{uuid.uuid4()}{pathlib.Path(selected_file_document_fake.file_name).suffix}",
        file_data=None
    )
    headers: Dict[str, Any] = {
        "Authorization": f"Bearer {selected_session_fake.access_token}"
    }
    response: Response = await main_context.client.post(
        url=url_path,
        headers=headers,
        data=file_document_creator_body.model_dump(mode="json", exclude={"file_data"}),
        files={"file_data": selected_file_document_data_fake}
    )

    content: Content[FileDocumentResponse] = Content[FileDocumentResponse](
        **response.json(),
        status_code=response.status_code
    )
    assert content.status_code == status.HTTP_201_CREATED
    assert content.data.name == file_document_creator_body.name
    assert content.data.description == file_document_creator_body.description
    assert content.data.document_type_id == DocumentTypeConstant.FILE
    assert content.data.account_id == file_document_creator_body.account_id
    assert content.data.file_data_hash == hashlib.sha256(
        selected_file_document_data_fake
    ).hexdigest()
    assert content.data.file_metadata is not None

    file_document: FileDocument = FileDocument(
        id=content.data.id,
        file_name=content.data.file_name,
        file_data_hash=content.data.file_data_hash,
    )
    main_context.all_seeder.file_document_seeder.file_document_fake.data.append(file_document)


@pytest.mark.asyncio
async def test__patch_one_by_id__should_patch_one_file_document__succeed(main_context: MainContext):
    selected_session_fake: Session = main_context.all_seeder.session_seeder.session_fake.data[0]
    selected_file_document_fake: FileDocument = main_context.all_seeder.file_document_seeder.file_document_fake.data[0]
    selected_file_document_data_fake: bytes = main_context.all_seeder.file_document_seeder.file_document_fake.file_data[
        0]
    selected_document_fake: Document = main_context.all_seeder.document_seeder.document_fake.data[0]
    file_document_patcher_body: PatchOneBody = PatchOneBody(
        name=f"patched.name{uuid.uuid4()}",
        description=f"patched.description{uuid.uuid4()}",
        account_id=selected_document_fake.account_id,
        file_name=f"patched.file_name{uuid.uuid4()}{pathlib.Path(selected_file_document_fake.file_name).suffix}",
        file_data=None
    )
    headers: Dict[str, Any] = {
        "Authorization": f"Bearer {selected_session_fake.access_token}"
    }
    response: Response = await main_context.client.patch(
        url=f"{url_path}/{selected_file_document_fake.id}",
        headers=headers,
        data=file_document_patcher_body.model_dump(mode="json", exclude={"file_data"}),
        files={"file_data": selected_file_document_data_fake}
    )

    content: Content[FileDocumentResponse] = Content[FileDocumentResponse](
        **response.json(),
        status_code=response.status_code
    )
    assert content.status_code == status.HTTP_200_OK
    assert content.data.name == file_document_patcher_body.name
    assert content.data.description == file_document_patcher_body.description
    assert content.data.document_type_id == DocumentTypeConstant.FILE
    assert content.data.account_id == file_document_patcher_body.account_id
    assert content.data.file_data_hash == hashlib.sha256(
        selected_file_document_data_fake
    ).hexdigest()
    assert content.data.file_metadata is not None


@pytest.mark.asyncio
async def test__delete_one_by_id__should_delete_one_file_document__succeed(main_context: MainContext):
    selected_document_fake: Document = main_context.all_seeder.document_seeder.document_fake.data[0]
    selected_file_document_fake: FileDocument = main_context.all_seeder.file_document_seeder.file_document_fake.data[0]
    selected_session_fake: Session = main_context.all_seeder.session_seeder.session_fake.data[0]
    headers: Dict[str, Any] = {
        "Authorization": f"Bearer {selected_session_fake.access_token}"
    }
    response: Response = await main_context.client.delete(
        url=f"{url_path}/{selected_file_document_fake.id}",
        headers=headers
    )

    content: Content[FileDocumentResponse] = Content[FileDocumentResponse](
        **response.json(),
        status_code=response.status_code
    )
    assert content.status_code == status.HTTP_200_OK
    assert content.data.id == selected_file_document_fake.id
    assert content.data.name == selected_document_fake.name
    assert content.data.description == selected_document_fake.description
    assert content.data.document_type_id == DocumentTypeConstant.FILE
    assert content.data.account_id == selected_document_fake.account_id
    assert content.data.file_name == selected_file_document_fake.file_name
    assert content.data.file_data_hash == selected_file_document_fake.file_data_hash
    assert content.data.file_metadata is None
    main_context.all_seeder.delete_many_file_document_by_id_cascade(selected_file_document_fake.id)
