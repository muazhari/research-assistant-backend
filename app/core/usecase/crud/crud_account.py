from uuid import UUID

from app.core.model.entity.account import Account
from app.infrastucture.gateway.client.account_transaction_service_client import account_transaction_service_client


def find_all() -> [Account]:
    accounts: [Account] = account_transaction_service_client.find_all()
    return accounts


def find_one_by_id(id: UUID) -> Account:
    found_account: Account = account_transaction_service_client.find_one_by_id(id)
    return found_account


def create_one(account: Account) -> Account:
    created_account = account_transaction_service_client.create_one(account)
    return created_account


def update_one_by_id(id: UUID, account: Account) -> Account:
    found_account: Account = account_transaction_service_client.update_one_by_id(id, account)
    return found_account


def delete_one_by_id(id: UUID, account: Account) -> Account:
    found_account: Account = account_transaction_service_client.delete_one_by_id(id, account)
    return found_account
