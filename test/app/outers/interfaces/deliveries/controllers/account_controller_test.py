import json
from typing import List

import pytest as pytest
import pytest_asyncio

from app.inners.models.entities.account import Account
from app.inners.models.value_objects.contracts.requests.managements.accounts.create_body import \
    CreateBody
from app.inners.models.value_objects.contracts.requests.managements.accounts.patch_body import \
    PatchBody
from app.inners.models.value_objects.contracts.responses.content import Content
from app.outers.repositories.account_repository import AccountRepository
from test.mock_data.account_mock_data import AccountMockData
from test.utilities.test_client_utility import get_async_client

account_repository = AccountRepository()
account_mock_data = AccountMockData()


@pytest_asyncio.fixture(scope="function", autouse=True)
async def run_around(request: pytest.FixtureRequest):
    for account in account_mock_data.data:
        await account_repository.create_one(Account(**account.dict()))

    yield

    for account in account_mock_data.data:
        if request.node.name == "test__delete_one_by_id__should_delete_one_account__success" \
                and account.id == account_mock_data.data[0].id:
            continue
        await account_repository.delete_one_by_id(account.id)


@pytest.mark.asyncio
async def test__read_all__should_return_all_accounts__success():
    async with get_async_client() as client:
        response = await client.get(
            url="api/v1/accounts"
        )
        assert response.status_code == 200
        content: Content[List[Account]] = Content[List[Account]](**response.json())
        assert all(account in content.data for account in account_mock_data.data)


@pytest.mark.asyncio
async def test__read_one_by_id__should_return_one_account__success():
    async with get_async_client() as client:
        response = await client.get(
            url=f"api/v1/accounts/{account_mock_data.data[0].id}"
        )
        assert response.status_code == 200
        content: Content[Account] = Content[Account](**response.json())
        assert content.data == account_mock_data.data[0]


@pytest.mark.asyncio
async def test__create_one__should_create_one_account__success():
    body: CreateBody = CreateBody(
        name="name2",
        email="email2",
        password="password2"
    )
    async with get_async_client() as client:
        response = await client.post(
            url="api/v1/accounts",
            json=json.loads(body.json())
        )
        assert response.status_code == 200
        content: Content[Account] = Content[Account](**response.json())
        assert content.data.name == body.name
        assert content.data.email == body.email
        assert content.data.password == body.password
        account_mock_data.data.append(content.data)


@pytest.mark.asyncio
async def test__patch_one_by_id__should_patch_one_account__success():
    body: PatchBody = PatchBody(
        name=f"{account_mock_data.data[0].name} patched",
        email=f"{account_mock_data.data[0].email} patched",
        password=f"{account_mock_data.data[0].password} patched"
    )
    async with get_async_client() as client:
        response = await client.patch(
            url=f"api/v1/accounts/{account_mock_data.data[0].id}",
            json=json.loads(body.json())
        )
        assert response.status_code == 200
        content: Content[Account] = Content[Account](**response.json())
        assert content.data.name == body.name
        assert content.data.email == body.email
        assert content.data.password == body.password
        account_mock_data.data[0] = content.data


@pytest.mark.asyncio
async def test__delete_one_by_id__should_delete_one_account__success():
    async with get_async_client() as client:
        response = await client.delete(
            url=f"api/v1/accounts/{account_mock_data.data[0].id}"
        )
        assert response.status_code == 200
        content: Content[Account] = Content[Account](**response.json())
        assert content.data == account_mock_data.data[0]
