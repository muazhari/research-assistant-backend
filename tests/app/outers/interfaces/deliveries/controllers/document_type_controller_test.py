import json
import json
import uuid

import pytest as pytest
from httpx import Response

from apps.inners.models.daos.document_type import DocumentType
from apps.inners.models.daos.session import Session
from apps.inners.models.dtos.contracts.content import Content
from apps.inners.models.dtos.contracts.requests.managements.document_types.patch_one_body import \
    PatchOneBody
from tests.conftest import MainTest

url_path: str = "/api/document-types"


@pytest.mark.asyncio
async def test__find_one_by_id__should__succeed(main_test: MainTest):
    selected_session_mock: Session = main_test.all_seeder.session_seeder.session_mock.data[0]
    id: str = "text"
    headers: dict = {
        "Authorization": f"Bearer {selected_session_mock.access_token}"
    }
    response: Response = await main_test.client.get(
        url=f"{url_path}/{id}",
        headers=headers
    )

    assert response.status_code == 200
    response_body: Content[DocumentType] = Content[DocumentType](**response.json())
    assert response_body.data.id == id


@pytest.mark.asyncio
async def test__patch_one_by_id__should_patch_one_document_type__succeed(main_test: MainTest):
    selected_session_mock: Session = main_test.all_seeder.session_seeder.session_mock.data[0]
    selected_document_type_mock: DocumentType = main_test.all_seeder.document_type_seeder.document_type_mock.data[0]
    document_type_patcher_body: PatchOneBody = PatchOneBody(
        id=selected_document_type_mock.id,
        description=f"description{uuid.uuid4()}",
    )
    headers: dict = {
        "Authorization": f"Bearer {selected_session_mock.access_token}"
    }
    response: Response = await main_test.client.patch(
        url=f"{url_path}/{selected_document_type_mock.id}",
        json=json.loads(document_type_patcher_body.json()),
        headers=headers
    )

    assert response.status_code == 200
    response_body: Content[DocumentType] = Content[DocumentType](**response.json())
    assert response_body.data.id == document_type_patcher_body.id
    assert response_body.data.description == document_type_patcher_body.description
