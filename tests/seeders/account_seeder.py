import bcrypt
from sqlalchemy.engine import Result
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from apps.inners.models.daos.account import Account
from tests.fakes.account_fake import AccountFake


class AccountSeeder:

    def __init__(
            self,
            account_fake: AccountFake
    ):
        self.account_fake: AccountFake = account_fake

    async def up(self, session: AsyncSession):
        for account in self.account_fake.data:
            account.password = bcrypt.hashpw(account.password.encode(), bcrypt.gensalt()).decode()
            session.add(account)

    async def down(self, session: AsyncSession):
        for account in self.account_fake.data:
            found_account_result: Result = await session.execute(
                select(Account).where(Account.id == account.id).limit(1)
            )
            found_account: Account = found_account_result.scalars().one()
            await session.delete(found_account)
