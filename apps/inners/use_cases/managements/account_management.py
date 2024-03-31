import uuid
from uuid import UUID

import bcrypt
from starlette.datastructures import State

from apps.inners.models.daos.account import Account
from apps.inners.models.dtos.contracts.requests.managements.accounts.create_one_body import CreateOneBody
from apps.inners.models.dtos.contracts.requests.managements.accounts.patch_one_body import PatchOneBody
from apps.outers.repositories.account_repository import AccountRepository


class AccountManagement:
    def __init__(
            self,
            account_repository: AccountRepository,
    ):
        self.account_repository: AccountRepository = account_repository

    async def find_one_by_id_with_authorization(self, state: State, id: UUID) -> Account:
        found_account: Account = await self.account_repository.find_one_by_id_and_account_id(
            session=state.session,
            id=id,
            account_id=state.authorized_session.account_id
        )
        return found_account

    async def find_one_by_email(self, state: State, email: str) -> Account:
        found_account: Account = await self.account_repository.find_one_by_email(
            session=state.session,
            email=email
        )
        return found_account

    async def create_one(self, state: State, body: CreateOneBody) -> Account:
        account_creator: Account = Account(**body.dict())
        account_creator.id = uuid.uuid4()
        account_creator.password = bcrypt.hashpw(account_creator.password.encode(), bcrypt.gensalt()).decode()
        created_account: Account = self.create_one_raw(
            state=state,
            account_creator=account_creator
        )
        return created_account

    def create_one_raw(self, state: State, account_creator: Account) -> Account:
        created_account: Account = self.account_repository.create_one(
            session=state.session,
            account_creator=account_creator
        )
        return created_account

    async def patch_one_by_id_with_authorization(self, state: State, id: UUID, body: PatchOneBody) -> Account:
        account_patcher: Account = Account(**body.dict())
        account_patcher.password = bcrypt.hashpw(account_patcher.password.encode(), bcrypt.gensalt()).decode()
        patched_account: Account = await self.patch_one_by_id_raw_with_authorization(
            state=state,
            id=id,
            account_patcher=account_patcher
        )
        return patched_account

    async def patch_one_by_id_raw_with_authorization(self, state: State, id: UUID, account_patcher: Account) -> Account:
        patched_account: Account = await self.account_repository.patch_one_by_id_and_account_id(
            session=state.session,
            id=id,
            account_id=state.authorized_session.account_id,
            account_patcher=account_patcher
        )
        return patched_account

    async def delete_one_by_id_with_authorization(self, state: State, id: UUID) -> Account:
        deleted_account: Account = await self.account_repository.delete_one_by_id_and_account_id(
            session=state.session,
            id=id,
            account_id=state.authorized_session.account_id
        )
        return deleted_account
