import uuid
from datetime import datetime

import pytest

from app.inner.model.entities.account import Account
from app.inner.model.entities.document import Document
from app.inner.model.entities.document_type import DocumentType
from app.inner.model.entities.text_document import TextDocument
from app.inner.model.entities.text_document import TextDocument
from app.outer.interfaces.deliveries.contracts.requests.entity_manager.text_document.create_one_request import \
    CreateOneRequest as TextDocumentCreateOneRequest
from app.outer.interfaces.deliveries.contracts.requests.entity_manager.text_document.patch_one_by_id_request import \
    PatchOneByIdRequest as TextDocumentPatchOneByIdRequest
from app.outer.interfaces.deliveries.contracts.requests.entity_manager.document.create_one_request import \
    CreateOneRequest as DocumentCreateOneRequest
from app.outer.interfaces.deliveries.contracts.requests.entity_manager.document.patch_one_by_id_request import \
    PatchOneByIdRequest as DocumentPatchOneByIdRequest
from app.outer.repositories.account_repository import account_repository
from app.outer.repositories.document_repository import document_repository
from app.outer.repositories.text_document_repository import text_document_repository
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
        name="test text_document_type name 0",
        description="test text_document_type description 0",
        updated_at=datetime.now(),
        created_at=datetime.now()
    ),
    DocumentType(
        id=uuid.uuid4(),
        name="test text_document_type name 0",
        description="test text_document_type description 0",
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

text_document_mocks = [
    TextDocument(
        id=uuid.uuid4(),
        document_id=document_mocks[0].id,
        text_content="test text_content 0",
    ),
    TextDocument(
        id=uuid.uuid4(),
        document_id=document_mocks[1].id,
        text_content="test text_content 1",
    )
]


def setup_function():
    for account, document_type, document, text_document in zip(account_mocks, document_type_mocks,
                                                              document_mocks,
                                                              text_document_mocks):
        account_repository.create_one(account.copy())
        document_type_repository.create_one(document_type.copy())
        document_repository.create_one(document.copy())
        text_document_repository.create_one(text_document.copy())


def teardown_function(function):
    for account, document_type, document, text_document in zip(account_mocks, document_type_mocks,
                                                              document_mocks,
                                                              text_document_mocks):
        if function.__name__ == "test_text_document_delete_one_by_id_success":
            if text_document.id == text_document_mocks[0].id:
                continue
        text_document_repository.delete_one_by_id(text_document.id)
        document_repository.delete_one_by_id(document.id)
        document_type_repository.delete_one_by_id(document_type.id)
        account_repository.delete_one_by_id(account.id)


def test_text_document_read_all_success():
    response = client.get("/api/v1/documents/texts")
    assert response.status_code == 200
    content = response.json()
    text_documents = [TextDocument(**text_document) for text_document in content["data"]]
    assert all(text_document_mock in text_documents for text_document_mock in text_document_mocks)


def test_text_document_read_one_by_id_success():
    response = client.get(f"/api/v1/documents/texts/{text_document_mocks[0].id}")
    assert response.status_code == 200
    content = response.json()
    text_document = TextDocument(**content["data"])
    assert text_document == text_document_mocks[0]


def test_text_document_create_one_success():
    document_mock = DocumentCreateOneRequest(
        name="test text_document name 2",
        description="test text_document description 2",
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

    text_document_mock = TextDocumentCreateOneRequest(
        document_id=document.id,
        text_content="test text_content 2",
    )

    text_document_response = client.post("/api/v1/documents/texts", data=text_document_mock.json(),
                                        headers={'Content-Type': 'application/json'})
    assert text_document_response.status_code == 200
    text_content = text_document_response.json()
    text_document = TextDocument(**text_content["data"])
    assert text_document.document_id == text_document_mock.document_id
    assert text_document.text_content == text_document_mock.text_content


def test_text_document_patch_one_by_id_success():
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

    text_document_mock = TextDocumentPatchOneByIdRequest(
        document_id=document.id,
        text_content=f"{text_document_mocks[0].text_content} patched",
    )

    response = client.patch(f"/api/v1/documents/texts/{text_document_mocks[0].id}", data=text_document_mock.json(),
                            headers={'Content-Type': 'application/json'})
    assert response.status_code == 200
    text_document_content = response.json()
    text_document = TextDocument(**text_document_content["data"])
    assert text_document.text_content == text_document_mock.text_content


def test_text_document_delete_one_by_id_success():
    response = client.delete(f"/api/v1/documents/texts/{text_document_mocks[0].id}")
    assert response.status_code == 200
    text_document_content = response.json()
    text_document = TextDocument(**text_document_content["data"])
    assert text_document == text_document_mocks[0]

    response = client.delete(f"/api/v1/documents/{document_mocks[0].id}")
    assert response.status_code == 200
    document_content = response.json()
    document = Document(**document_content["data"])
    assert document == document_mocks[0]
