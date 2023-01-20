import os
import uuid
from datetime import datetime

import pytest

from app.inner.model.entities.account import Account
from app.outer.interfaces.deliveries.contracts.requests.entity_manager.account.create_one_request import \
    CreateOneRequest
from app.outer.interfaces.deliveries.contracts.requests.entity_manager.account.patch_one_by_id_request import \
    PatchOneByIdRequest
from app.outer.repositories.account_repository import account_repository
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


def setup_function():
    for account in account_mocks:
        account_repository.create_one(account.copy())


def teardown_function(function):
    for account in account_mocks:
        if function.__name__ == "test_account_delete_one_by_id_success" and account.id == account_mocks[0].id:
            return
        account_repository.delete_one_by_id(account.id)


def test_account_read_all_success():
    response = client.get("/api/v1/accounts")
    assert response.status_code == 200
    content = response.json()
    accounts = [Account(**account) for account in content["data"]]
    assert all(account_mock in accounts for account_mock in account_mocks)


def test_account_read_one_by_id_success():
    response = client.get(f"/api/v1/accounts/{account_mocks[0].id}")
    assert response.status_code == 200
    content = response.json()
    account = Account(**content["data"])
    assert account in account_mocks


def test_account_create_one_success():
    request_mock: CreateOneRequest = CreateOneRequest(
        name="test account name 2",
        email="test.account.email.2@example.com",
        password="test password password 2"
    )

    response = client.post("/api/v1/accounts", data=request_mock.json(),
                           headers={'Content-Type': 'application/json'})
    assert response.status_code == 200
    content = response.json()
    account = Account(**content["data"])
    assert account.name == request_mock.name
    assert account.email == request_mock.email
    assert account.password == request_mock.password


def test_account_patch_one_by_id_success():
    request_mock: PatchOneByIdRequest = PatchOneByIdRequest(
        name=f"{account_mocks[0].name} patched",
        email=f"patched.{account_mocks[0].email}",
        password=f"{account_mocks[0].password} patched"
    )
    response = client.patch(f"/api/v1/accounts/{account_mocks[0].id}", data=request_mock.json(),
                            headers={'Content-Type': 'application/json'})
    assert response.status_code == 200
    content = response.json()
    account = Account(**content["data"])
    assert account.name == request_mock.name
    assert account.email == request_mock.email
    assert account.password == request_mock.password


def test_account_delete_one_by_id_success():
    response = client.delete(f"/api/v1/accounts/{account_mocks[0].id}")
    assert response.status_code == 200
    content = response.json()
    account = Account(**content["data"])
    assert account == account_mocks[0]
