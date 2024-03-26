import uuid
from uuid import UUID

import bcrypt
from sqlalchemy import exc
from starlette import status
from starlette.datastructures import State

from apps.inners.models.daos.account import Account
from apps.inners.models.dtos.contracts.requests.managements.accounts.create_one_body import CreateOneBody
from apps.inners.models.dtos.contracts.requests.managements.accounts.patch_one_body import PatchOneBody
from apps.inners.models.dtos.contracts.result import Result
from apps.outers.repositories.account_repository import AccountRepository


class AccountManagement:
    def __init__(
            self,
            account_repository: AccountRepository,
    ):
        self.account_repository: AccountRepository = account_repository

    async def find_one_by_id(self, state: State, id: UUID) -> Result[Account]:
        try:
            found_account: Account = await self.account_repository.find_one_by_id(
                session=state.session,
                id=id
            )
            result: Result[Account] = Result(
                status_code=status.HTTP_200_OK,
                message="AccountManagement.find_one_by_id: Succeed.",
                data=found_account,
            )
        except exc.NoResultFound:
            result: Result[Account] = Result(
                status_code=status.HTTP_404_NOT_FOUND,
                message="AccountManagement.find_one_by_id: Failed, account is not found.",
                data=None,
            )
        return result

    async def find_one_by_email(self, state: State, email: str) -> Result[Account]:
        try:
            found_account: Account = await self.account_repository.find_one_by_email(
                session=state.session,
                email=email
            )
            result: Result[Account] = Result(
                status_code=status.HTTP_200_OK,
                message="AccountManagement.find_one_by_email: Succeed.",
                data=found_account,
            )
        except exc.NoResultFound:
            result: Result[Account] = Result(
                status_code=status.HTTP_404_NOT_FOUND,
                message="AccountManagement.find_one_by_email: Failed, account is not found.",
                data=None,
            )
        return result

    async def find_one_by_email_and_password(self, state: State, email: str, password: str) -> Result[Account]:
        try:
            found_account: Account = await self.account_repository.find_one_by_email_and_password(
                session=state.session,
                email=email,
                password=password
            )
            result: Result[Account] = Result(
                status_code=status.HTTP_200_OK,
                message="AccountManagement.find_one_by_email_and_password: Succeed.",
                data=found_account,
            )
        except exc.NoResultFound:
            result: Result[Account] = Result(
                status_code=status.HTTP_404_NOT_FOUND,
                message="AccountManagement.find_one_by_email_and_password: Failed, account is not found.",
                data=None,
            )
        return result

    async def create_one(self, state: State, body: CreateOneBody) -> Result[Account]:
        account_creator: Account = Account(**body.dict())
        account_creator.id = uuid.uuid4()
        account_creator.password = bcrypt.hashpw(account_creator.password.encode(), bcrypt.gensalt()).decode()
        created_account: Account = await self.account_repository.create_one(
            session=state.session,
            account_creator=account_creator
        )
        result: Result[Account] = Result(
            status_code=status.HTTP_201_CREATED,
            message="AccountManagement.create_one: Succeed.",
            data=created_account,
        )
        return result

    async def create_one_raw(self, state: State, account_creator: Account) -> Result[Account]:
        created_account: Account = await self.account_repository.create_one(
            session=state.session,
            account_creator=account_creator
        )
        result: Result[Account] = Result(
            status_code=status.HTTP_201_CREATED,
            message="AccountManagement.create_one_raw: Succeed.",
            data=created_account,
        )
        return result

    async def patch_one_by_id(self, state: State, id: UUID, body: PatchOneBody) -> Result[Account]:
        try:
            account_patcher: Account = Account(**body.dict())
            account_patcher.password = bcrypt.hashpw(account_patcher.password.encode(), bcrypt.gensalt()).decode()
            patched_account: Account = await self.account_repository.patch_one_by_id(
                session=state.session,
                id=id,
                account_patcher=account_patcher
            )
            result: Result[Account] = Result(
                status_code=status.HTTP_200_OK,
                message="AccountManagement.patch_one_by_id: Succeed.",
                data=patched_account,
            )
        except exc.NoResultFound:
            result: Result[Account] = Result(
                status_code=status.HTTP_404_NOT_FOUND,
                message="AccountManagement.patch_one_by_id: Failed, account is not found.",
                data=None,
            )
        return result

    async def patch_one_by_id_raw(self, state: State, id: UUID, account_patcher: Account) -> Result[Account]:
        patched_account: Account = await self.account_repository.patch_one_by_id(
            session=state.session,
            id=id,
            account_patcher=account_patcher
        )
        result: Result[Account] = Result(
            status_code=status.HTTP_200_OK,
            message="AccountManagement.patch_one_by_id_raw: Succeed.",
            data=patched_account,
        )
        return result

    async def delete_one_by_id(self, state: State, id: UUID) -> Result[Account]:
        try:
            deleted_account: Account = await self.account_repository.delete_one_by_id(
                session=state.session,
                id=id
            )
            result: Result[Account] = Result(
                status_code=status.HTTP_200_OK,
                message="AccountManagement.delete_one_by_id: Succeed.",
                data=deleted_account,
            )
        except exc.NoResultFound:
            result: Result[Account] = Result(
                status_code=status.HTTP_404_NOT_FOUND,
                message="AccountManagement.delete_one_by_id: Failed, account is not found.",
                data=None,
            )
        return result
