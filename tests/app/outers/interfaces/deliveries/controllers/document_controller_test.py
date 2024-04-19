import uuid
from typing import Dict, Any
from typing import List

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
from apps.inners.models.dtos.contracts.requests.managements.documents.search_body import SearchBody
from tests.main_context import MainContext

url_path: str = "/api/documents"


@pytest.mark.asyncio
async def test__search__should__succeed(main_context: MainContext):
    selected_session_fake: Session = main_context.all_seeder.session_seeder.session_fake.data[0]
    selected_document_fake: Document = main_context.all_seeder.document_seeder.document_fake.data[0]

    search_body: SearchBody = SearchBody(
        id=str(selected_document_fake.id),
        name=selected_document_fake.name,
        description=selected_document_fake.description,
        document_type_id=str(selected_document_fake.document_type_id),
        account_id=None,
    )
    headers: Dict[str, Any] = {
        "Authorization": f"Bearer {selected_session_fake.access_token}"
    }
    params: Dict[str, Any] = {
        "size": len(main_context.all_seeder.document_seeder.document_fake.data)
    }
    response: Response = await main_context.client.post(
        url=f"{url_path}/searches",
        headers=headers,
        params=params,
        json=search_body.model_dump(mode="json")
    )

    content: Content[List[Document]] = Content[List[Document]](
        **response.json(),
        status_code=response.status_code
    )
    assert content.status_code == status.HTTP_200_OK
    assert len(content.data) == 1
    assert content.data[0] == selected_document_fake


@pytest.mark.asyncio
async def test__find_many_with_pagination__should__succeed(main_context: MainContext):
    selected_session_fake: Session = main_context.all_seeder.session_seeder.session_fake.data[0]
    selected_document_fakes: List[Document] = []
    for document_fake in main_context.all_seeder.document_seeder.document_fake.data:
        if document_fake.account_id == selected_session_fake.account_id:
            selected_document_fakes.append(document_fake)

    headers: Dict[str, Any] = {
        "Authorization": f"Bearer {selected_session_fake.access_token}"
    }
    params: Dict[str, Any] = {
        "page_position": 1,
        "page_size": len(selected_document_fakes)
    }
    response: Response = await main_context.client.get(
        url=url_path,
        headers=headers,
        params=params
    )

    content: Content[List[Document]] = Content[List[Document]](
        **response.json(),
        status_code=response.status_code
    )
    assert content.status_code == status.HTTP_200_OK
    assert len(content.data) == len(selected_document_fakes)
    for document in content.data:
        for selected_document_fake in selected_document_fakes:
            if document.id == selected_document_fake.id:
                assert document == selected_document_fake


@pytest.mark.asyncio
async def test__find_one_by_id__should__succeed(main_context: MainContext):
    selected_document_fake: Document = main_context.all_seeder.document_seeder.document_fake.data[0]
    selected_session_fake: Session = main_context.all_seeder.session_seeder.session_fake.data[0]
    headers: Dict[str, Any] = {
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
    headers: Dict[str, Any] = {
        "Authorization": f"Bearer {selected_session_fake.access_token}"
    }
    response: Response = await main_context.client.post(
        url=url_path,
        json=document_creator_body.model_dump(mode="json"),
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

    main_context.all_seeder.document_seeder.document_fake.data.append(content.data)


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
    headers: Dict[str, Any] = {
        "Authorization": f"Bearer {selected_session_fake.access_token}"
    }
    response: Response = await main_context.client.patch(
        url=f"{url_path}/{selected_document_fake.id}",
        json=document_patcher_body.model_dump(mode="json"),
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
    headers: Dict[str, Any] = {
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
