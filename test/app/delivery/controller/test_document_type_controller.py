import uuid
from datetime import datetime

import pytest

from app.inner.model.entities.document_type import DocumentType
from app.outer.interfaces.deliveries.contracts.requests.entity_manager.document_type.create_one_request import \
    CreateOneRequest
from app.outer.interfaces.deliveries.contracts.requests.entity_manager.document_type.patch_one_by_id_request import \
    PatchOneByIdRequest
from app.outer.repositories.document_type_repository import document_type_repository
from test.utility.client import get_test_client_app

client = get_test_client_app()

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


def setup_function():
    for document_type in document_type_mocks:
        document_type_repository.create_one(document_type.copy())


def teardown_function(function):
    for document_type in document_type_mocks:
        if function.__name__ == "test_document_type_delete_one_by_id_success":
            if document_type.id == document_type_mocks[0].id:
                continue
        document_type_repository.delete_one_by_id(document_type.id)


def test_document_type_read_all_success():
    response = client.get("/api/v1/documents/types")
    assert response.status_code == 200
    content = response.json()
    document_types = [DocumentType(**document_type) for document_type in content["data"]]
    assert all(document_type_mock in document_types for document_type_mock in document_type_mocks)


def test_document_type_read_one_by_id_success():
    response = client.get(f"/api/v1/documents/types/{document_type_mocks[0].id}")
    assert response.status_code == 200
    content = response.json()
    document_type = DocumentType(**content["data"])
    assert document_type == document_type_mocks[0]


def test_document_type_create_one_success():
    document_type_mock = CreateOneRequest(
        name="test document_type name 2",
        description="test document_type description 2",
    )

    response = client.post("/api/v1/documents/types", data=document_type_mock.json(),
                           headers={'Content-Type': 'application/json'})
    assert response.status_code == 200
    content = response.json()
    document_type = DocumentType(**content["data"])
    assert document_type.name == document_type_mock.name
    assert document_type.description == document_type_mock.description


def test_document_type_patch_one_by_id_success():
    document_type_mock = PatchOneByIdRequest(
        name=f"{document_type_mocks[0].name} patched",
        description=f"{document_type_mocks[0].description} patched",
    )

    response = client.patch(f"/api/v1/documents/types/{document_type_mocks[0].id}",
                            data=document_type_mock.json(),
                            headers={'Content-Type': 'application/json'})
    assert response.status_code == 200
    content = response.json()
    document_type = DocumentType(**content["data"])
    assert document_type.name == document_type_mock.name
    assert document_type.description == document_type_mock.description


def test_document_type_delete_one_by_id_success():
    response = client.delete(f"/api/v1/documents/types/{document_type_mocks[0].id}")
    assert response.status_code == 200
    content = response.json()
    document_type = DocumentType(**content["data"])
    assert document_type == document_type_mocks[0]
