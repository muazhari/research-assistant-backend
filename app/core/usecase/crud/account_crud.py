from uuid import UUID

from app.core.model.entity.account import Account
from app.infrastucture.gateway.client.account_transaction_service_client import account_transaction_service_client


def find_all() -> [Account]:
    async with await account_transaction_service_client.find_all() as response:
        assert response.status == 200
        accounts: [dict] = await response.json()
        account_entities = [Account(**account) for account in accounts]
        return account_entities


def find_one_by_id(id: UUID) -> Account:
    async with await account_transaction_service_client.find_one_by_id(
            id
    ) as response:
        found_account: dict = await response.json()
        found_account_entity = Account(**found_account)
        return found_account_entity


def create_one(account: Account) -> Account:
    async with await account_transaction_service_client.save_one(
            account.dict()
    ) as response:
        saved_account: dict = await response.json()
        saved_account_entity = Account(**saved_account)
        return saved_account_entity


def update_one_by_id(id: UUID, account: Account) -> Account:
    async with await account_transaction_service_client.update_one_by_id(
            id,
            account.dict()
    ) as response:
        updated_account: dict = await response.json()
        updated_account_entity = Account(**updated_account)
        return updated_account_entity


def delete_one_by_id(id: UUID) -> Account:
    async with await account_transaction_service_client.delete_one_by_id(
            id
    ) as response:
        deleted_account: dict = await response.json()
        deleted_account_entity = Account(**deleted_account)
        return deleted_account_entity
