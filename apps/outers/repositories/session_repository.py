from uuid import UUID

import sqlalchemy
from sqlalchemy import exc
from sqlalchemy.engine import ScalarResult
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from apps.inners.exceptions import repository_exception
from apps.inners.models.daos.session import Session


class SessionRepository:

    def __init__(self):
        pass

    async def find_one_by_id(self, session: AsyncSession, id: UUID) -> Session:
        try:
            found_session_result: ScalarResult = await session.exec(
                select(Session).where(Session.id == id).limit(1)
            )
            found_session: Session = found_session_result.one()
        except sqlalchemy.exc.NoResultFound:
            raise repository_exception.NotFound()

        return found_session

    async def find_one_by_account_id(self, session: AsyncSession, account_id: UUID) -> Session:
        try:
            found_session_result: ScalarResult = await session.exec(
                select(Session).where(Session.account_id == account_id).limit(1)
            )
            found_session: Session = found_session_result.one()
        except sqlalchemy.exc.NoResultFound:
            raise repository_exception.NotFound()

        return found_session

    async def find_one_by_access_token(self, session: AsyncSession, access_token: str) -> Session:
        try:
            found_session_result: ScalarResult = await session.exec(
                select(Session).where(Session.access_token == access_token).limit(1)
            )
            found_session: Session = found_session_result.one()
        except sqlalchemy.exc.NoResultFound:
            raise repository_exception.NotFound()

        return found_session

    async def find_one_by_refresh_token(self, session: AsyncSession, refresh_token: str) -> Session:
        try:
            found_session_result: ScalarResult = await session.exec(
                select(Session).where(Session.refresh_token == refresh_token).limit(1)
            )
            found_session: Session = found_session_result.one()
        except sqlalchemy.exc.NoResultFound:
            raise repository_exception.NotFound()

        return found_session

    def create_one(self, session: AsyncSession, session_creator: Session) -> Session:
        try:
            session.add(session_creator)
        except sqlalchemy.exc.IntegrityError:
            raise repository_exception.IntegrityError()

        return session_creator

    async def patch_one_by_id(self, session: AsyncSession, id: UUID, session_patcher: Session) -> Session:
        found_session: Session = await self.find_one_by_id(
            session=session,
            id=id
        )
        found_session.patch_from(session_patcher.dict(exclude_none=True))

        return found_session

    async def delete_one_by_id(self, session: AsyncSession, id: UUID) -> Session:
        found_session: Session = await self.find_one_by_id(
            session=session,
            id=id
        )
        await session.delete(found_session)

        return found_session
