import bcrypt
from sqlmodel import select
from sqlalchemy import Result
from sqlmodel.ext.asyncio.session import AsyncSession

from app.inners.models.daos.account import Account
from test.mocks.account_mock import AccountMock


class AccountSeeder:

    def __init__(
            self,
            account_mock: AccountMock
    ):
        self.account_mock: AccountMock = account_mock

    async def up(self, session: AsyncSession):
        for account in self.account_mock.data:
            account.password = bcrypt.hashpw(account.password.encode(), bcrypt.gensalt()).decode()
            session.add(account)

    async def down(self, session: AsyncSession):
        for account in self.account_mock.data:
            found_account_result: Result = await session.execute(
                select(Account).where(Account.id == account.id).limit(1)
            )
            found_account: Account = found_account_result.scalars().one()
            await session.delete(found_account)
