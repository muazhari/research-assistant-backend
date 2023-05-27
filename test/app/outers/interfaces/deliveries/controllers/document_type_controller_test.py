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

test_client = get_async_client()
document_type_repository = DocumentTypeRepository()
document_type_mock_data = DocumentTypeMockData()
data = document_type_mock_data.get_data()


@pytest_asyncio.fixture(scope="function", autouse=True)
async def run_around(request: pytest.FixtureRequest):
    for document_type in data["document_type"]:
        await document_type_repository.create_one(DocumentType(**document_type.dict()))

    yield

    for document_type in data["document_type"]:
        if request.node.name == "test__delete_one_by_id__should_delete_one_document_type__success" \
                and document_type.id == data["document_type"][0].id:
            continue
        await document_type_repository.delete_one_by_id(document_type.id)


@pytest.mark.asyncio
async def test__read_all__should_return_all_document_types__success():
    response = await test_client.get(
        url="api/v1/document-types"
    )
    assert response.status_code == 200
    content: Content[List[DocumentType]] = Content[List[DocumentType]](**response.json())
    assert all([document_type in content.data for document_type in data["document_type"]])


@pytest.mark.asyncio
async def test__read_one_by_id__should_return_one_document_type__success():
    response = await test_client.get(
        url=f"api/v1/document-types/{data['document_type'][0].id}"
    )
    assert response.status_code == 200
    content: Content[DocumentType] = Content[DocumentType](**response.json())
    assert content.data == data["document_type"][0]


@pytest.mark.asyncio
async def test__create_one__should_create_one_document_type__success():
    document_type_create: CreateBody = CreateBody(
        name="name2",
        description="description2",
    )
    response = await test_client.post(
        url="api/v1/document-types",
        json=json.loads(document_type_create.json())
    )
    assert response.status_code == 200
    content: Content[DocumentType] = Content[DocumentType](**response.json())
    assert content.data.name == document_type_create.name
    assert content.data.description == document_type_create.description
    data["document_type"].append(content.data)


@pytest.mark.asyncio
async def test__patch_one_by_id__should_patch_one_document_type__success():
    document_type_patch: PatchBody = PatchBody(
        name=f"{data['document_type'][0].name} patched",
        description=f"{data['document_type'][0].description} patched",
    )
    response = await test_client.patch(
        url=f"api/v1/document-types/{data['document_type'][0].id}",
        json=json.loads(document_type_patch.json())
    )
    assert response.status_code == 200
    content: Content[DocumentType] = Content[DocumentType](**response.json())
    assert content.data.name == document_type_patch.name
    assert content.data.description == document_type_patch.description
    data["document_type"][0] = content.data


@pytest.mark.asyncio
async def test__delete_one_by_id__should_delete_one_document_type__success():
    response = await test_client.delete(
        url=f"api/v1/document-types/{data['document_type'][0].id}"
    )
    assert response.status_code == 200
    content: Content[DocumentType] = Content[DocumentType](**response.json())
    assert content.data == data["document_type"][0]
