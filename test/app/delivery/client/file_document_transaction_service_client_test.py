import asyncio
import base64
from copy import deepcopy
from time import sleep
from uuid import UUID

import pytest

from app.core.model.entity.file_document import FileDocument
from app.infrastucture.gateway.client.file_document_transaction_service_client import \
    file_document_transaction_service_client
from app.infrastucture.utility.java_bytes import b64_encode

file_document_mocks: [FileDocument] = [
    FileDocument(
        name="test file_document 0",
        description="test description 0",
        document_type_id=UUID("eb5adc50-df69-4bd0-b4d0-e300d3ff7561"),
        account_id=UUID("db5adc50-df69-4bd0-b4d0-e300d3ff7560"),
        file_document_id=UUID("ad2cbad1-6ccf-48e3-bb92-bc9961bc01a0"),
        file_name="test file name 0",
        file_extension="test file extension 0",
        file_bytes=b64_encode("test file bytes 0"),
    ),
    FileDocument(
        name="test file_document 1",
        description="test description 1",
        document_type_id=UUID("eb5adc50-df69-4bd0-b4d0-e300d3ff7561"),
        account_id=UUID("db5adc50-df69-4bd0-b4d0-e300d3ff7560"),
        file_document_id=UUID("ad2cbad1-6ccf-48e3-bb92-bc9961bc01a1"),
        file_name="test file name 1",
        file_extension="test file extension 1",
        file_bytes=b64_encode("test file bytes 1"),
    )
]


async def do_before_each_tests():
    global file_document_mocks

    for index, file_document in enumerate(file_document_mocks):
        async with await file_document_transaction_service_client.save_one(file_document.dict()) as response:
            assert response.status == 200
            file_document = await response.json()
            file_document_entity = FileDocument(**file_document)
            file_document_mocks[index] = file_document_entity


async def do_after_each_tests():
    global file_document_mocks

    for file_document in file_document_mocks:
        async with await file_document_transaction_service_client.delete_one_by_id(file_document.id) as response:
            assert response.status == 200


@pytest.fixture(autouse=True)
@pytest.mark.asyncio
async def run_around_tests():
    await do_before_each_tests()
    yield
    await do_after_each_tests()


# test find all file_documents
@pytest.mark.asyncio
async def test_find_all_file_document():
    async with await file_document_transaction_service_client.find_all() as response:
        assert response.status == 200
        file_documents: [dict] = await response.json()
        file_document_entities = [FileDocument(**file_document) for file_document in file_documents]
        assert file_documents is not None
        assert len(file_document_entities) > 0
        assert isinstance(file_document_entities[0], FileDocument)
        assert all([file_document_mock in file_document_entities for file_document_mock in file_document_mocks])


# test save one file_document
@pytest.mark.asyncio
async def test_save_one_file_document():
    file_document_to_save = FileDocument(
        name="test file_document 2",
        description="test description 2",
        document_type_id=UUID("eb5adc50-df69-4bd0-b4d0-e300d3ff7561"),
        account_id=UUID("db5adc50-df69-4bd0-b4d0-e300d3ff7560"),
        file_document_id=UUID("ad2cbad1-6ccf-48e3-bb92-bc9961bc01a2"),
        file_name="test file name 2",
        file_extension="test file extension 2",
        file_bytes=b64_encode("test file bytes 2"),
    )

    async with await file_document_transaction_service_client.save_one(
            file_document_to_save.dict()
    ) as response:
        assert response.status == 200
        saved_file_document: dict = await response.json()
        assert saved_file_document is not None
        assert isinstance(FileDocument(**saved_file_document), FileDocument)

        saved_file_document_entity = FileDocument(**saved_file_document)
        file_document_to_save.id = deepcopy(saved_file_document_entity.id)
        file_document_to_save.updated_at = deepcopy(saved_file_document_entity.updated_at)
        file_document_to_save.created_at = deepcopy(saved_file_document_entity.created_at)
        assert saved_file_document_entity.__eq__(file_document_to_save)

        file_document_mocks.append(saved_file_document_entity)


# test find one file_document by id
@pytest.mark.asyncio
async def test_find_one_file_document_by_id():
    to_find_file_document = file_document_mocks[0]
    file_document_id: UUID = to_find_file_document.id

    async with await file_document_transaction_service_client.find_one_by_id(
            file_document_id
    ) as response:
        assert response.status == 200
        found_file_document: dict = await response.json()
        assert found_file_document is not None
        found_file_document_entity = FileDocument(**found_file_document)
        assert found_file_document_entity.__eq__(to_find_file_document)


# test update one file_document by id
@pytest.mark.asyncio
async def test_update_one_file_document():
    file_document_to_update = file_document_mocks[0]
    file_document_to_update.name = "updated test file_document 2"
    file_document_to_update.description = "updated test description 2"
    file_document_to_update.document_type_id = UUID("eb5adc50-df69-4bd0-b4d0-e300d3ff7561")
    file_document_to_update.account_id = UUID("db5adc50-df69-4bd0-b4d0-e300d3ff7560")
    file_document_to_update.file_name = "updated test file name 2"
    file_document_to_update.file_extension = "updated test file extension 2"
    file_document_to_update.file_bytes = b64_encode("updated test file bytes 2")

    async with await file_document_transaction_service_client.update_one_by_id(
            file_document_to_update.id,
            file_document_to_update.dict()
    ) as response:
        assert response.status == 200
        updated_file_document: dict = await response.json()
        assert updated_file_document is not None

        updated_file_document_entity = FileDocument(**updated_file_document)
        file_document_to_update.updated_at = deepcopy(updated_file_document_entity.updated_at)
        assert updated_file_document_entity.__eq__(file_document_to_update)

        file_document_mocks[0] = updated_file_document_entity


# test delete one file_document by id
@pytest.mark.asyncio
async def test_delete_one_file_document_by_id():
    file_document_to_delete = file_document_mocks[0]

    async with await file_document_transaction_service_client.delete_one_by_id(
            file_document_to_delete.id
    ) as response:
        assert response.status == 200
        deleted_file_document: dict = await response.json()
        assert deleted_file_document is not None

        deleted_file_document_entity = FileDocument(**deleted_file_document)
        assert deleted_file_document_entity.__eq__(file_document_to_delete)

        file_document_mocks.pop(0)
