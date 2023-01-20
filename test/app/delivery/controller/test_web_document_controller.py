import uuid
from datetime import datetime

import pytest

from app.inner.model.entities.account import Account
from app.inner.model.entities.document import Document
from app.inner.model.entities.document_type import DocumentType
from app.inner.model.entities.web_document import WebDocument
from app.inner.model.entities.web_document import WebDocument
from app.outer.interfaces.deliveries.contracts.requests.entity_manager.web_document.create_one_request import \
    CreateOneRequest as WebDocumentCreateOneRequest
from app.outer.interfaces.deliveries.contracts.requests.entity_manager.web_document.patch_one_by_id_request import \
    PatchOneByIdRequest as WebDocumentPatchOneByIdRequest
from app.outer.interfaces.deliveries.contracts.requests.entity_manager.document.create_one_request import \
    CreateOneRequest as DocumentCreateOneRequest
from app.outer.interfaces.deliveries.contracts.requests.entity_manager.document.patch_one_by_id_request import \
    PatchOneByIdRequest as DocumentPatchOneByIdRequest
from app.outer.repositories.account_repository import account_repository
from app.outer.repositories.document_repository import document_repository
from app.outer.repositories.web_document_repository import web_document_repository
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
        name="test web_document_type name 0",
        description="test web_document_type description 0",
        updated_at=datetime.now(),
        created_at=datetime.now()
    ),
    DocumentType(
        id=uuid.uuid4(),
        name="test web_document_type name 0",
        description="test web_document_type description 0",
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

web_document_mocks = [
    WebDocument(
        id=uuid.uuid4(),
        document_id=document_mocks[0].id,
        web_url="test web_url 0",
    ),
    WebDocument(
        id=uuid.uuid4(),
        document_id=document_mocks[1].id,
        web_url="test web_url 1",
    )
]


def setup_function():
    for account, document_type, document, web_document in zip(account_mocks, document_type_mocks,
                                                              document_mocks,
                                                              web_document_mocks):
        account_repository.create_one(account.copy())
        document_type_repository.create_one(document_type.copy())
        document_repository.create_one(document.copy())
        web_document_repository.create_one(web_document.copy())


def teardown_function(function):
    for account, document_type, document, web_document in zip(account_mocks, document_type_mocks,
                                                              document_mocks,
                                                              web_document_mocks):
        if function.__name__ == "test_web_document_delete_one_by_id_success":
            if web_document.id == web_document_mocks[0].id:
                continue
        web_document_repository.delete_one_by_id(web_document.id)
        document_repository.delete_one_by_id(document.id)
        document_type_repository.delete_one_by_id(document_type.id)
        account_repository.delete_one_by_id(account.id)


def test_web_document_read_all_success():
    response = client.get("/api/v1/documents/webs")
    assert response.status_code == 200
    content = response.json()
    web_documents = [WebDocument(**web_document) for web_document in content["data"]]
    assert all(web_document_mock in web_documents for web_document_mock in web_document_mocks)


def test_web_document_read_one_by_id_success():
    response = client.get(f"/api/v1/documents/webs/{web_document_mocks[0].id}")
    assert response.status_code == 200
    content = response.json()
    web_document = WebDocument(**content["data"])
    assert web_document == web_document_mocks[0]


def test_web_document_create_one_success():
    document_mock = DocumentCreateOneRequest(
        name="test web_document name 2",
        description="test web_document description 2",
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

    web_document_mock = WebDocumentCreateOneRequest(
        document_id=document.id,
        web_url="test web_url 2",
    )

    web_document_response = client.post("/api/v1/documents/webs", data=web_document_mock.json(),
                                        headers={'Content-Type': 'application/json'})
    assert web_document_response.status_code == 200
    web_content = web_document_response.json()
    web_document = WebDocument(**web_content["data"])
    assert web_document.document_id == web_document_mock.document_id
    assert web_document.web_url == web_document_mock.web_url


def test_web_document_patch_one_by_id_success():
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

    web_document_mock = WebDocumentPatchOneByIdRequest(
        document_id=document.id,
        web_url=f"{web_document_mocks[0].web_url} patched",
    )

    response = client.patch(f"/api/v1/documents/webs/{web_document_mocks[0].id}", data=web_document_mock.json(),
                            headers={'Content-Type': 'application/json'})
    assert response.status_code == 200
    web_document_content = response.json()
    web_document = WebDocument(**web_document_content["data"])
    assert web_document.web_url == web_document_mock.web_url


def test_web_document_delete_one_by_id_success():
    response = client.delete(f"/api/v1/documents/webs/{web_document_mocks[0].id}")
    assert response.status_code == 200
    web_document_content = response.json()
    web_document = WebDocument(**web_document_content["data"])
    assert web_document == web_document_mocks[0]

    response = client.delete(f"/api/v1/documents/{document_mocks[0].id}")
    assert response.status_code == 200
    document_content = response.json()
    document = Document(**document_content["data"])
    assert document == document_mocks[0]
