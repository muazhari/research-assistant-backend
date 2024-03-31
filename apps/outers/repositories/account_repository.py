from uuid import UUID

import sqlalchemy
from sqlalchemy import exc
from sqlalchemy.engine import Result
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from apps.inners.models.daos.account import Account
from apps.outers.exceptions import repository_exception


class AccountRepository:

    def __init__(self):
        pass

    async def find_one_by_id(self, session: AsyncSession, id: UUID) -> Account:
        try:
            found_account_result: Result = await session.execute(
                select(Account).where(Account.id == id).limit(1)
            )
            found_account: Account = found_account_result.scalars().one()
        except sqlalchemy.exc.NoResultFound:
            raise repository_exception.NotFound()

        return found_account

    async def find_one_by_email_and_password(self, session: AsyncSession, email: str, password: str) -> Account:
        try:
            found_account_result: Result = await session.execute(
                select(Account).where(Account.email == email).where(Account.password == password).limit(1)
            )
            found_account: Account = found_account_result.scalars().one()
        except sqlalchemy.exc.NoResultFound:
            raise repository_exception.NotFound()

        return found_account

    async def find_one_by_email(self, session: AsyncSession, email: str) -> Account:
        try:
            found_account_result: Result = await session.execute(
                select(Account).where(Account.email == email).limit(1)
            )
            found_account: Account = found_account_result.scalars().one()
        except sqlalchemy.exc.NoResultFound:
            raise repository_exception.NotFound()

        return found_account

    def create_one(self, session: AsyncSession, account_creator: Account) -> Account:
        try:
            session.add(account_creator)
        except sqlalchemy.exc.IntegrityError:
            raise repository_exception.IntegrityError()

        return account_creator

    async def patch_one_by_id(self, session: AsyncSession, id: UUID, account_patcher: Account) -> Account:
        found_account: Account = await self.find_one_by_id(
            session=session,
            id=id
        )
        found_account.patch_from(account_patcher.dict(exclude_none=True))

        return found_account

    async def delete_one_by_id(self, session: AsyncSession, id: UUID) -> Account:
        found_account: Account = await self.find_one_by_id(
            session=session,
            id=id
        )
        await session.delete(found_account)
        return found_account
