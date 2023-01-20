import uuid
from datetime import datetime

import pytest

from app.inner.model.entities.account import Account
from app.inner.model.entities.document import Document
from app.inner.model.entities.document_type import DocumentType
from app.outer.interfaces.deliveries.contracts.requests.entity_manager.document.create_one_request import \
    CreateOneRequest
from app.outer.interfaces.deliveries.contracts.requests.entity_manager.document.patch_one_by_id_request import \
    PatchOneByIdRequest
from app.outer.repositories.account_repository import account_repository
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


def setup_function():
    for account, document_type, document in zip(account_mocks, document_type_mocks, document_mocks):
        account_repository.create_one(account.copy())
        document_type_repository.create_one(document_type.copy())
        document_repository.create_one(document.copy())


def teardown_function(function):
    for account, document_type, document in zip(account_mocks, document_type_mocks, document_mocks):
        if function.__name__ == "test_document_delete_one_by_id_success":
            if document.id == document_mocks[0].id:
                continue
        document_repository.delete_one_by_id(document.id)
        document_type_repository.delete_one_by_id(document_type.id)
        account_repository.delete_one_by_id(account.id)


def test_document_read_all_success():
    response = client.get("/api/v1/documents")
    assert response.status_code == 200
    content = response.json()
    documents = [Document(**document) for document in content["data"]]
    assert all(document_mock in documents for document_mock in document_mocks)


def test_document_read_one_by_id_success():
    response = client.get(f"/api/v1/documents/{document_mocks[0].id}")
    assert response.status_code == 200
    content = response.json()
    document = Document(**content["data"])
    assert document == document_mocks[0]


def test_document_create_one_success():
    document_mock = CreateOneRequest(
        name="test document name 2",
        description="test document description 2",
        document_type_id=document_type_mocks[0].id,
        account_id=account_mocks[0].id
    )

    response = client.post("/api/v1/documents", data=document_mock.json(),
                           headers={'Content-Type': 'application/json'})
    assert response.status_code == 200
    content = response.json()
    document = Document(**content["data"])
    assert document.name == document_mock.name
    assert document.description == document_mock.description
    assert document.document_type_id == document_mock.document_type_id
    assert document.account_id == document_mock.account_id


def test_document_patch_one_by_id_success():
    document_mock = PatchOneByIdRequest(
        name=f"{document_mocks[0].name} patched",
        description=f"{document_mocks[0].description} patched",
        document_type_id=document_type_mocks[1].id,
        account_id=account_mocks[1].id
    )

    response = client.patch(f"/api/v1/documents/{document_mocks[0].id}", data=document_mock.json(),
                            headers={'Content-Type': 'application/json'})
    assert response.status_code == 200
    content = response.json()
    document = Document(**content["data"])
    assert document.name == document_mock.name
    assert document.description == document_mock.description
    assert document.document_type_id == document_mock.document_type_id
    assert document.account_id == document_mock.account_id


def test_document_delete_one_by_id_success():
    response = client.delete(f"/api/v1/documents/{document_mocks[0].id}")
    assert response.status_code == 200
    content = response.json()
    document = Document(**content["data"])
    assert document == document_mocks[0]
