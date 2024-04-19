import uuid
from typing import Dict, Any

import pytest as pytest
from httpx import Response
from starlette import status

from apps.inners.models.daos.document_type import DocumentType
from apps.inners.models.daos.session import Session
from apps.inners.models.dtos.content import Content
from apps.inners.models.dtos.contracts.requests.managements.document_types.patch_one_body import \
    PatchOneBody
from tests.main_context import MainContext

url_path: str = "/api/document-types"


@pytest.mark.asyncio
async def test__find_one_by_id__should__succeed(main_context: MainContext):
    selected_session_fake: Session = main_context.all_seeder.session_seeder.session_fake.data[0]
    id: str = "text"
    headers: Dict[str, Any] = {
        "Authorization": f"Bearer {selected_session_fake.access_token}"
    }
    response: Response = await main_context.client.get(
        url=f"{url_path}/{id}",
        headers=headers
    )

    content: Content[DocumentType] = Content[DocumentType](
        **response.json(),
        status_code=response.status_code
    )
    assert content.status_code == status.HTTP_200_OK
    assert content.data.id == id


@pytest.mark.asyncio
async def test__patch_one_by_id__should_patch_one_document_type__succeed(main_context: MainContext):
    selected_session_fake: Session = main_context.all_seeder.session_seeder.session_fake.data[0]
    selected_document_type_fake: DocumentType = main_context.all_seeder.document_type_seeder.document_type_fake.data[0]
    document_type_patcher_body: PatchOneBody = PatchOneBody(
        id=selected_document_type_fake.id,
        description=f"description{uuid.uuid4()}",
    )
    headers: Dict[str, Any] = {
        "Authorization": f"Bearer {selected_session_fake.access_token}"
    }
    response: Response = await main_context.client.patch(
        url=f"{url_path}/{selected_document_type_fake.id}",
        json=document_type_patcher_body.model_dump(mode="json"),
        headers=headers
    )

    content: Content[DocumentType] = Content[DocumentType](
        **response.json(),
        status_code=response.status_code
    )
    assert content.status_code == status.HTTP_200_OK
    assert content.data.id == document_type_patcher_body.id
    assert content.data.description == document_type_patcher_body.description
