import json
from typing import List

import pytest as pytest
import pytest_asyncio

from app.inners.models.entities.document_type import DocumentType
from app.inners.models.value_objects.contracts.requests.managements.document_types.create_body import \
    CreateBody
from app.inners.models.value_objects.contracts.requests.managements.document_types.patch_body import \
    PatchBody
from app.inners.models.value_objects.contracts.responses.content import Content
from app.outers.repositories.document_type_repository import DocumentTypeRepository
from test.mock_data.document_type_mock_data import DocumentTypeMockData
from test.utilities.test_client_utility import get_async_client

document_type_repository = DocumentTypeRepository()
document_type_mock_data = DocumentTypeMockData()


@pytest_asyncio.fixture(scope="function", autouse=True)
async def run_around(request: pytest.FixtureRequest):
    for document_type in document_type_mock_data.data:
        await document_type_repository.create_one(DocumentType(**document_type.dict()))

    yield

    for document_type in document_type_mock_data.data:
        if request.node.name == "test__delete_one_by_id__should_delete_one_document_type__success" \
                and document_type.id == document_type_mock_data.data[0].id:
            continue
        await document_type_repository.delete_one_by_id(document_type.id)


@pytest.mark.asyncio
async def test__read_all__should_return_all_document_types__success():
    async with get_async_client() as client:
        response = await client.get(
            url="api/v1/document-types"
        )
        assert response.status_code == 200
        content: Content[List[DocumentType]] = Content[List[DocumentType]](**response.json())
        assert all(document_type in content.data for document_type in document_type_mock_data.data)


@pytest.mark.asyncio
async def test__read_one_by_id__should_return_one_document_type__success():
    async with get_async_client() as client:
        response = await client.get(
            url=f"api/v1/document-types/{document_type_mock_data.data[0].id}"
        )
        assert response.status_code == 200
        content: Content[DocumentType] = Content[DocumentType](**response.json())
        assert content.data == document_type_mock_data.data[0]


@pytest.mark.asyncio
async def test__create_one__should_create_one_document_type__success():
    body: CreateBody = CreateBody(
        name="name2",
        description="description2",
    )
    async with get_async_client() as client:
        response = await client.post(
            url="api/v1/document-types",
            json=json.loads(body.json())
        )
        assert response.status_code == 200
        content: Content[DocumentType] = Content[DocumentType](**response.json())
        assert content.data.name == body.name
        assert content.data.description == body.description
        document_type_mock_data.data.append(content.data)


@pytest.mark.asyncio
async def test__patch_one_by_id__should_patch_one_document_type__success():
    body: PatchBody = PatchBody(
        name=f"{document_type_mock_data.data[0].name} patched",
        description=f"{document_type_mock_data.data[0].description} patched",
    )
    async with get_async_client() as client:
        response = await client.patch(
            url=f"api/v1/document-types/{document_type_mock_data.data[0].id}",
            json=json.loads(body.json())
        )
        assert response.status_code == 200
        content: Content[DocumentType] = Content[DocumentType](**response.json())
        assert content.data.name == body.name
        assert content.data.description == body.description
        document_type_mock_data.data[0] = content.data


@pytest.mark.asyncio
async def test__delete_one_by_id__should_delete_one_document_type__success():
    async with get_async_client() as client:
        response = await client.delete(
            url=f"api/v1/document-types/{document_type_mock_data.data[0].id}"
        )
    assert response.status_code == 200
    content: Content[DocumentType] = Content[DocumentType](**response.json())
    assert content.data == document_type_mock_data.data[0]
