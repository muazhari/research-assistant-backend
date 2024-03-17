import json
import json
import uuid

import pytest as pytest
from httpx import Response

from app.inners.models.daos.document_type import DocumentType
from app.inners.models.dtos.contracts.content import Content
from app.inners.models.dtos.contracts.requests.managements.document_types.patch_one_body import \
    PatchOneBody
from test.conftest import MainTest

url_path: str = "/api/document-types"


@pytest.mark.asyncio
async def test__find_one_by_id__should_return_one_document_type__succeed(run_around: MainTest):
    id: str = "text"
    response: Response = await run_around.client.get(
        url=f"{url_path}/{id}"
    )
    assert response.status_code == 200
    response_body: Content[DocumentType] = Content[DocumentType](**response.json())
    assert response_body.data.id == id


@pytest.mark.asyncio
async def test__patch_one_by_id__should_patch_one_document_type__succeed(run_around: MainTest):
    selected_document_type_mock: DocumentType = run_around.all_seeder.document_type_seeder.document_type_mock.data[0]
    document_type_to_patch_body: PatchOneBody = PatchOneBody(
        id=selected_document_type_mock.id,
        description=f"description{uuid.uuid4()}",
    )
    response: Response = await run_around.client.patch(
        url=f"{url_path}/{selected_document_type_mock.id}",
        json=json.loads(document_type_to_patch_body.json())
    )
    assert response.status_code == 200
    response_body: Content[DocumentType] = Content[DocumentType](**response.json())
    assert response_body.data.id == document_type_to_patch_body.id
    assert response_body.data.description == document_type_to_patch_body.description
