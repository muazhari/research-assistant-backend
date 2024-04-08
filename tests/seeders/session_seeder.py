from sqlalchemy.engine import Result
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from apps.inners.models.daos.session import Session
from tests.fakes.session_fake import SessionFake


class SessionSeeder:

    def __init__(
            self,
            session_fake: SessionFake,
    ):
        self.session_fake: SessionFake = session_fake

    async def up(self, session: AsyncSession):
        for session_dao in self.session_fake.data:
            session.add(session_dao)

    async def down(self, session: AsyncSession):
        for session_dao in self.session_fake.data:
            found_session_result: Result = await session.execute(
                select(Session).where(Session.id == session_dao.id).limit(1)
            )
            found_session: Session = found_session_result.scalars().one()
            await session.delete(found_session)
