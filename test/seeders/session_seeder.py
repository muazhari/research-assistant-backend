from sqlmodel import select
from sqlmodel.engine.result import Result
from sqlmodel.ext.asyncio.session import AsyncSession

from app.inners.models.daos.session import Session
from app.outers.datastores.one_datastore import OneDatastore
from test.mocks.session_mock import SessionMock


class SessionSeeder:

    def __init__(
            self,
            session_mock: SessionMock,
            one_datastore: OneDatastore,
    ):
        self.session_mock: SessionMock = session_mock
        self.one_datastore: OneDatastore = one_datastore

    async def up(self, session: AsyncSession):
        for session_dao in self.session_mock.data:
            session.add(session_dao)

    async def down(self, session: AsyncSession):
        for session_dao in self.session_mock.data:
            found_session_result: Result = await session.execute(
                select(Session).where(Session.id == session_dao.id).limit(1)
            )
            found_session: Session = found_session_result.scalars().one()
            await session.delete(found_session)
