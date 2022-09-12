import asyncio
from copy import deepcopy
from time import sleep
from uuid import UUID

import pytest

from app.core.model.entity.document import Document
from app.infrastucture.gateway.client.document_transaction_service_client import document_transaction_service_client

document_mocks: [Document] = [
    Document(
        name="test document 0",
        description="test description 0",
        document_type_id=UUID("eb5adc50-df69-4bd0-b4d0-e300d3ff7561"),
        account_id=UUID("db5adc50-df69-4bd0-b4d0-e300d3ff7561")
    ),
    Document(
        name="test document 1",
        description="test description 1",
        document_type_id=UUID("eb5adc50-df69-4bd0-b4d0-e300d3ff7562"),
        account_id=UUID("db5adc50-df69-4bd0-b4d0-e300d3ff7561")
    )
]


async def do_before_each_tests():
    global document_mocks

    for index, document in enumerate(document_mocks):
        async with await document_transaction_service_client.save_one(document.dict()) as response:
            assert response.status == 200
            document = await response.json()
            document_entity = Document(**document)
            document_mocks[index] = document_entity


async def do_after_each_tests():
    global document_mocks

    for document in document_mocks:
        async with await document_transaction_service_client.delete_one_by_id(document.id) as response:
            assert response.status == 200


@pytest.fixture(autouse=True)
@pytest.mark.asyncio
async def run_around_tests():
    await do_before_each_tests()
    yield
    await do_after_each_tests()


# test find all documents
@pytest.mark.asyncio
async def test_find_all_document():
    async with await document_transaction_service_client.find_all() as response:
        assert response.status == 200
        documents: [dict] = await response.json()
        document_entities = [Document(**document) for document in documents]
        assert documents is not None
        assert len(document_entities) > 0
        assert isinstance(document_entities[0], Document)
        assert all([document_mock in document_entities for document_mock in document_mocks])


# test save one document
@pytest.mark.asyncio
async def test_save_one_document():
    document_to_save = Document(
        name="test document 2",
        description="test description 2",
        document_type_id=UUID("eb5adc50-df69-4bd0-b4d0-e300d3ff7563"),
        account_id=UUID("db5adc50-df69-4bd0-b4d0-e300d3ff7561")
    )

    async with await document_transaction_service_client.save_one(
            document_to_save.dict()
    ) as response:
        assert response.status == 200
        saved_document: dict = await response.json()
        assert saved_document is not None
        assert isinstance(Document(**saved_document), Document)

        saved_document_entity = Document(**saved_document)
        document_to_save.id = deepcopy(saved_document_entity.id)
        document_to_save.updated_at = deepcopy(saved_document_entity.updated_at)
        document_to_save.created_at = deepcopy(saved_document_entity.created_at)
        assert saved_document_entity.__eq__(document_to_save)

        document_mocks.append(saved_document_entity)


# test find one document by id
@pytest.mark.asyncio
async def test_find_one_document_by_id():
    to_find_document = document_mocks[0]
    document_id: UUID = to_find_document.id

    async with await document_transaction_service_client.find_one_by_id(
            document_id
    ) as response:
        assert response.status == 200
        found_document: dict = await response.json()
        assert found_document is not None
        found_document_entity = Document(**found_document)
        assert found_document_entity.__eq__(to_find_document)


# test update one document by id
@pytest.mark.asyncio
async def test_update_one_document():
    document_to_update = document_mocks[0]
    document_to_update.name = "updated test document 2"
    document_to_update.description = "updated test description 2"
    document_to_update.document_type_id = UUID("eb5adc50-df69-4bd0-b4d0-e300d3ff7563")
    document_to_update.account_id = UUID("db5adc50-df69-4bd0-b4d0-e300d3ff7562")

    async with await document_transaction_service_client.update_one_by_id(
            document_to_update.id,
            document_to_update.dict()
    ) as response:
        assert response.status == 200
        updated_document: dict = await response.json()
        assert updated_document is not None

        updated_document_entity = Document(**updated_document)
        document_to_update.updated_at = deepcopy(updated_document_entity.updated_at)
        assert updated_document_entity.__eq__(document_to_update)

        document_mocks[0] = updated_document_entity


# test delete one document by id
@pytest.mark.asyncio
async def test_delete_one_document_by_id():
    document_to_delete = document_mocks[0]

    async with await document_transaction_service_client.delete_one_by_id(
            document_to_delete.id
    ) as response:
        assert response.status == 200
        deleted_document: dict = await response.json()
        assert deleted_document is not None

        deleted_document_entity = Document(**deleted_document)
        assert deleted_document_entity.__eq__(document_to_delete)

        document_mocks.pop(0)
