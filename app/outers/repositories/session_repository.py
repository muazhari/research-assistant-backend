from uuid import UUID

from sqlmodel import select
from sqlmodel.engine.result import Result
from sqlmodel.ext.asyncio.session import AsyncSession

from app.inners.models.daos.session import Session


class SessionRepository:

    def __init__(self):
        pass

    async def find_one_by_id(self, session: AsyncSession, id: UUID) -> Session:
        found_session_result: Result = await session.execute(
            select(Session).where(Session.id == id).limit(1)
        )
        found_session: Session = found_session_result.scalars().one()
        return found_session

    async def find_one_by_access_token(self, session: AsyncSession, access_token: str) -> Session:
        found_session_result: Result = await session.execute(
            select(Session).where(Session.access_token == access_token).limit(1)
        )
        found_session: Session = found_session_result.scalars().one()
        return found_session

    async def find_one_by_refresh_token(self, session: AsyncSession, refresh_token: str) -> Session:
        found_session_result: Result = await session.execute(
            select(Session).where(Session.refresh_token == refresh_token).limit(1)
        )
        found_session: Session = found_session_result.scalars().one()
        return found_session

    async def create_one(self, session: AsyncSession, session_to_create: Session) -> Session:
        session.add(session_to_create)
        return session_to_create

    async def patch_one_by_id(self, session: AsyncSession, id: UUID, session_to_patch: Session) -> Session:
        found_session: Session = await self.find_one_by_id(
            session=session,
            id=id
        )
        found_session.patch_from(session_to_patch.dict())
        return found_session

    async def delete_one_by_id(self, session: AsyncSession, id: UUID) -> Session:
        found_session: Session = await self.find_one_by_id(
            session=session,
            id=id
        )
        await session.delete(found_session)
        return found_session
