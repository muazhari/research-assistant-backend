from copy import deepcopy
from uuid import UUID

import pytest

from app.inner.model.entities.account import Account
from app.outer.interfaces.gateways.client import \
    account_atlas_service_client

account_mocks: [Account] = [
    Account(
        name="test account 0",
        email="test0@example.com",
        password="test password 0"
    ),
    Account(
        name="test account 1",
        email="test0@example.com",
        password="test password 1"
    )
]


async def do_before_each_tests():
    global account_mocks

    for index, account in enumerate(account_mocks):
        async with await account_atlas_service_client.save_one(account.dict()) as response:
            assert response.status == 200
            account_json = await response.json()
            account_entity = Account(**account_json)
            account_mocks[index] = account_entity


async def do_after_each_tests():
    global account_mocks

    for account in account_mocks:
        async with await account_atlas_service_client.delete_one_by_id(account.id) as response:
            assert response.status == 200


@pytest.fixture(autouse=True)
@pytest.mark.asyncio
async def run_around_tests():
    await do_before_each_tests()
    yield
    await do_after_each_tests()


# test find all accounts
@pytest.mark.asyncio
async def test_find_all_account():
    async with await account_atlas_service_client.find_all() as response:
        assert response.status == 200
        accounts: [dict] = await response.json()
        account_entities = [Account(**account) for account in accounts]
        assert accounts is not None
        assert len(account_entities) > 0
        assert isinstance(account_entities[0], Account)
        assert all([account_mock in account_entities for account_mock in account_mocks])


# test find one account by id
@pytest.mark.asyncio
async def test_find_one_account_by_id():
    to_find_account = account_mocks[0]
    account_id: UUID = to_find_account.id

    async with await account_atlas_service_client.find_one_by_id(
            account_id
    ) as response:
        assert response.status == 200
        found_account: dict = await response.json()
        assert found_account is not None
        found_account_entity = Account(**found_account)
        assert found_account_entity == to_find_account


# test save one account
@pytest.mark.asyncio
async def test_save_one_account():
    account_to_save = Account(
        name="test account 2",
        email="test2@example.com",
        password="test password 2"
    )

    async with await account_atlas_service_client.save_one(
            account_to_save.dict()
    ) as response:
        assert response.status == 200
        saved_account: dict = await response.json()
        assert saved_account is not None
        assert isinstance(Account(**saved_account), Account)

        saved_account_entity = Account(**saved_account)
        account_to_save.id = deepcopy(saved_account_entity.id)
        account_to_save.updated_at = deepcopy(saved_account_entity.updated_at)
        account_to_save.created_at = deepcopy(saved_account_entity.created_at)
        assert saved_account_entity == account_to_save

        account_mocks.append(saved_account_entity)


# test update one account by id
@pytest.mark.asyncio
async def test_update_one_account():
    account_to_update = account_mocks[0]
    account_to_update.name = "updated test account 0"
    account_to_update.email = "updated.test0@example.com"
    account_to_update.password = "updated test password 0"

    async with await account_atlas_service_client.update_one_by_id(
            account_to_update.id,
            account_to_update.dict()
    ) as response:
        assert response.status == 200
        updated_account: dict = await response.json()
        assert updated_account is not None

        updated_account_entity = Account(**updated_account)
        account_to_update.updated_at = deepcopy(updated_account_entity.updated_at)
        assert updated_account_entity == account_to_update

        account_mocks[0] = updated_account_entity


# test delete one account by id
@pytest.mark.asyncio
async def test_delete_one_account_by_id():
    account_to_delete = account_mocks[0]

    async with await account_atlas_service_client.delete_one_by_id(
            account_to_delete.id
    ) as response:
        assert response.status == 200
        deleted_account: dict = await response.json()
        assert deleted_account is not None

        deleted_account_entity = Account(**deleted_account)
        assert deleted_account_entity == account_to_delete

        account_mocks.pop(0)
