import uuid
from datetime import datetime

import pytest

from app.inner.model.entities.account import Account
from app.inner.model.entities.document import Document
from app.inner.model.entities.document_process import DocumentProcess
from app.inner.model.entities.document_type import DocumentType
from app.outer.interfaces.deliveries.contracts.requests.entity_manager.document_process.create_one_request import \
    CreateOneRequest
from app.outer.interfaces.deliveries.contracts.requests.entity_manager.document_process.patch_one_by_id_request import \
    PatchOneByIdRequest
from app.outer.repositories.account_repository import account_repository
from app.outer.repositories.document_process_repository import document_process_repository
from app.outer.repositories.document_repository import document_repository
from app.outer.repositories.document_type_repository import document_type_repository
from test.utility.client import get_test_client_app

client = get_test_client_app()

account_mocks: [Account] = [
    Account(
        id=uuid.uuid4(),
        name="test account name 0",
        email="test.email.0@example.com",
        password="test password 0",
        updated_at=datetime.now(),
        created_at=datetime.now()
    ),
    Account(
        id=uuid.uuid4(),
        name="test account name 1",
        email="test.email.1@example.com",
        password="test account password 1",
        updated_at=datetime.now(),
        created_at=datetime.now()
    )
]

document_type_mocks: [DocumentType] = [
    DocumentType(
        id=uuid.uuid4(),
        name="test document_type name 0",
        description="test document_type description 0",
        updated_at=datetime.now(),
        created_at=datetime.now()
    ),
    DocumentType(
        id=uuid.uuid4(),
        name="test document_type name 0",
        description="test document_type description 0",
        updated_at=datetime.now(),
        created_at=datetime.now()
    )
]

document_mocks: [Document] = [
    Document(
        id=uuid.uuid4(),
        name="test document name 0",
        description="test document description 0",
        document_type_id=document_type_mocks[0].id,
        account_id=account_mocks[0].id,
        updated_at=datetime.now(),
        created_at=datetime.now()
    ),
    Document(
        id=uuid.uuid4(),
        name="test document name 1",
        description="test document description 1",
        document_type_id=document_type_mocks[1].id,
        account_id=account_mocks[1].id,
        updated_at=datetime.now(),
        created_at=datetime.now()
    )
]
document_process_mocks: [DocumentProcess] = [
    DocumentProcess(
        id=uuid.uuid4(),
        initial_document_id=document_mocks[0].id,
        final_document_id=document_mocks[1].id,
        process_duration=0,
        updated_at=datetime.now(),
        created_at=datetime.now()
    ),
    DocumentProcess(
        id=uuid.uuid4(),
        initial_document_id=document_mocks[1].id,
        final_document_id=document_mocks[0].id,
        process_duration=1,
        updated_at=datetime.now(),
        created_at=datetime.now()
    )
]


def setup_function():
    for account, document_type, document in zip(account_mocks, document_type_mocks, document_mocks):
        account_repository.create_one(account.copy())
        document_type_repository.create_one(document_type.copy())
        document_repository.create_one(document.copy())

    for document_process in document_process_mocks:
        document_process_repository.create_one(document_process.copy())


def teardown_function(function):
    for document_process in document_process_mocks:
        if function.__name__ == "test_document_process_delete_one_by_id_success":
            if document_process.id == document_process_mocks[0].id:
                continue
        document_process_repository.delete_one_by_id(document_process.id)

    for account, document_type, document, document_process in zip(account_mocks, document_type_mocks, document_mocks,
                                                                  document_process_mocks):
        document_repository.delete_one_by_id(document.id)
        account_repository.delete_one_by_id(account.id)
        document_type_repository.delete_one_by_id(document_type.id)


def test_document_process_read_all_success():
    response = client.get("/api/v1/documents/processes")
    assert response.status_code == 200
    content = response.json()
    document_processes = [DocumentProcess(**document_process) for document_process in content["data"]]
    assert all(document_process_mock in document_processes for document_process_mock in document_process_mocks)


def test_document_process_read_one_by_id_success():
    response = client.get(f"/api/v1/documents/processes/{document_process_mocks[0].id}")
    assert response.status_code == 200
    content = response.json()
    document_process = DocumentProcess(**content["data"])
    assert document_process == document_process_mocks[0]


def test_document_process_create_one_success():
    document_process_mock = CreateOneRequest(
        initial_document_id=document_mocks[0].id,
        final_document_id=document_mocks[1].id,
        process_duration=0
    )

    response = client.post("/api/v1/documents/processes", data=document_process_mock.json(),
                           headers={'Content-Type': 'application/json'})
    assert response.status_code == 200
    content = response.json()
    document_process = DocumentProcess(**content["data"])
    assert document_process.initial_document_id == document_process_mock.initial_document_id
    assert document_process.final_document_id == document_process_mock.final_document_id
    assert document_process.process_duration == document_process_mock.process_duration


def test_document_process_patch_one_by_id_success():
    document_process_mock = PatchOneByIdRequest(
        initial_document_id=document_process_mocks[0].initial_document_id,
        final_document_id=document_process_mocks[0].final_document_id,
        process_duration=document_process_mocks[0].process_duration + 1
    )

    response = client.patch(f"/api/v1/documents/processes/{document_process_mocks[0].id}",
                            data=document_process_mock.json(),
                            headers={'Content-Type': 'application/json'})
    assert response.status_code == 200
    content = response.json()
    document_process = DocumentProcess(**content["data"])
    assert document_process.initial_document_id == document_process_mock.initial_document_id
    assert document_process.final_document_id == document_process_mock.final_document_id
    assert document_process.process_duration == document_process_mock.process_duration


def test_document_process_delete_one_by_id_success():
    response = client.delete(f"/api/v1/documents/processes/{document_process_mocks[0].id}")
    assert response.status_code == 200
    content = response.json()
    document_process = DocumentProcess(**content["data"])
    assert document_process == document_process_mocks[0]
