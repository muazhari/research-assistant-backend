import uuid
from datetime import datetime

import pytest

from app.inner.model.entities.account import Account
from app.inner.model.entities.document import Document
from app.inner.model.entities.document_type import DocumentType
from app.inner.model.entities.file_document import FileDocument
from app.inner.model.entities.file_document import FileDocument
from app.outer.interfaces.deliveries.contracts.requests.entity_manager.file_document.create_one_request import \
    CreateOneRequest as FileDocumentCreateOneRequest
from app.outer.interfaces.deliveries.contracts.requests.entity_manager.file_document.patch_one_by_id_request import \
    PatchOneByIdRequest as FileDocumentPatchOneByIdRequest
from app.outer.interfaces.deliveries.contracts.requests.entity_manager.document.create_one_request import \
    CreateOneRequest as DocumentCreateOneRequest
from app.outer.interfaces.deliveries.contracts.requests.entity_manager.document.patch_one_by_id_request import \
    PatchOneByIdRequest as DocumentPatchOneByIdRequest
from app.outer.repositories.account_repository import account_repository
from app.outer.repositories.document_repository import document_repository
from app.outer.repositories.file_document_repository import file_document_repository
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
        name="test file_document_type name 0",
        description="test file_document_type description 0",
        updated_at=datetime.now(),
        created_at=datetime.now()
    ),
    DocumentType(
        id=uuid.uuid4(),
        name="test file_document_type name 0",
        description="test file_document_type description 0",
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

file_document_mocks = [
    FileDocument(
        id=uuid.uuid4(),
        document_id=document_mocks[0].id,
        file_name="test file_name 0",
        file_extension="test file_extension 0",
        file_bytes="test file_bytes 0",
    ),
    FileDocument(
        id=uuid.uuid4(),
        document_id=document_mocks[1].id,
        file_name="test file_name 1",
        file_extension="test file_extension 1",
        file_bytes="test file_bytes 1",
    )
]


def setup_function():
    for account, document_type, document, file_document in zip(account_mocks, document_type_mocks,
                                                               document_mocks,
                                                               file_document_mocks):
        account_repository.create_one(account.copy())
        document_type_repository.create_one(document_type.copy())
        document_repository.create_one(document.copy())
        file_document_repository.create_one(file_document.copy())


def teardown_function(function):
    for account, document_type, document, file_document in zip(account_mocks, document_type_mocks,
                                                               document_mocks,
                                                               file_document_mocks):
        if function.__name__ == "test_file_document_delete_one_by_id_success":
            if file_document.id == file_document_mocks[0].id:
                continue
        file_document_repository.delete_one_by_id(file_document.id)
        document_repository.delete_one_by_id(document.id)
        document_type_repository.delete_one_by_id(document_type.id)
        account_repository.delete_one_by_id(account.id)


def test_file_document_read_all_success():
    response = client.get("/api/v1/documents/files")
    assert response.status_code == 200
    content = response.json()
    file_documents = [FileDocument(**file_document) for file_document in content["data"]]
    assert all(file_document_mock in file_documents for file_document_mock in file_document_mocks)


def test_file_document_read_one_by_id_success():
    response = client.get(f"/api/v1/documents/files/{file_document_mocks[0].id}")
    assert response.status_code == 200
    content = response.json()
    file_document = FileDocument(**content["data"])
    assert file_document == file_document_mocks[0]


def test_file_document_create_one_success():
    document_mock = DocumentCreateOneRequest(
        name="test file_document name 2",
        description="test file_document description 2",
        document_type_id=document_mocks[0].document_type_id,
        account_id=document_mocks[0].account_id
    )

    document_response = client.post("/api/v1/documents", data=document_mock.json(),
                                    headers={'Content-Type': 'application/json'})
    assert document_response.status_code == 200
    document_content = document_response.json()
    document = Document(**document_content["data"])
    assert document.name == document_mock.name
    assert document.description == document_mock.description
    assert document.document_type_id == document_mock.document_type_id
    assert document.account_id == document_mock.account_id

    file_document_mock = FileDocumentCreateOneRequest(
        document_id=document.id,
        file_name="test file_name 2",
        file_extension="test file_extension 2",
        file_bytes="test file_bytes 2",
    )

    file_document_response = client.post("/api/v1/documents/files", data=file_document_mock.json(),
                                         headers={'Content-Type': 'application/json'})
    assert file_document_response.status_code == 200
    file_name = file_document_response.json()
    file_document = FileDocument(**file_name["data"])
    assert file_document.document_id == file_document_mock.document_id
    assert file_document.file_name == file_document_mock.file_name
    assert file_document.file_extension == file_document_mock.file_extension
    assert file_document.file_bytes == file_document_mock.file_bytes


def test_file_document_patch_one_by_id_success():
    document_mock = DocumentPatchOneByIdRequest(
        name=f"{document_mocks[0].name} patched",
        description=f"{document_mocks[0].description} patched",
        document_type_id=document_mocks[0].document_type_id,
        account_id=document_mocks[0].account_id
    )

    document_response = client.patch(f"/api/v1/documents/{document_mocks[0].id}", data=document_mock.json(),
                                     headers={'Content-Type': 'application/json'})
    assert document_response.status_code == 200
    document_content = document_response.json()
    document = Document(**document_content["data"])
    assert document.name == document_mock.name
    assert document.description == document_mock.description
    assert document.document_type_id == document_mock.document_type_id
    assert document.account_id == document_mock.account_id

    file_document_mock = FileDocumentPatchOneByIdRequest(
        document_id=document.id,
        file_name=f"{file_document_mocks[0].file_name} patched",
        file_extension=f"{file_document_mocks[0].file_extension} patched",
        file_bytes=f"{file_document_mocks[0].file_bytes} patched",
    )

    response = client.patch(f"/api/v1/documents/files/{file_document_mocks[0].id}", data=file_document_mock.json(),
                            headers={'Content-Type': 'application/json'})
    assert response.status_code == 200
    file_document_content = response.json()
    file_document = FileDocument(**file_document_content["data"])
    assert file_document.file_name == file_document_mock.file_name
    assert file_document.file_extension == file_document_mock.file_extension
    assert file_document.file_bytes == file_document_mock.file_bytes


def test_file_document_delete_one_by_id_success():
    response = client.delete(f"/api/v1/documents/files/{file_document_mocks[0].id}")
    assert response.status_code == 200
    file_document_content = response.json()
    file_document = FileDocument(**file_document_content["data"])
    assert file_document == file_document_mocks[0]

    response = client.delete(f"/api/v1/documents/{document_mocks[0].id}")
    assert response.status_code == 200
    document_content = response.json()
    document = Document(**document_content["data"])
    assert document == document_mocks[0]
