import uuid
from uuid import UUID

from starlette.datastructures import State

from apps.inners.models.daos.session import Session
from apps.inners.models.dtos.contracts.requests.managements.sessions.create_one_body import CreateOneBody
from apps.inners.models.dtos.contracts.requests.managements.sessions.patch_one_body import PatchOneBody
from apps.outers.repositories.session_repository import SessionRepository


class SessionManagement:
    def __init__(
            self,
            session_repository: SessionRepository,
    ):
        self.session_repository: SessionRepository = session_repository

    async def find_one_by_id(self, state: State, id: UUID) -> Session:
        found_session: Session = await self.session_repository.find_one_by_id(
            session=state.session,
            id=id
        )
        return found_session

    async def find_one_by_account_id(self, state: State, account_id: UUID) -> Session:
        found_session: Session = await self.session_repository.find_one_by_account_id(
            session=state.session,
            account_id=account_id
        )
        return found_session

    async def find_one_by_access_token(self, state: State, access_token: str) -> Session:
        found_session: Session = await self.session_repository.find_one_by_access_token(
            session=state.session,
            access_token=access_token
        )
        return found_session

    async def find_one_by_refresh_token(self, state: State, refresh_token: str) -> Session:
        found_session: Session = await self.session_repository.find_one_by_refresh_token(
            session=state.session,
            refresh_token=refresh_token
        )
        return found_session

    async def create_one(self, state: State, body: CreateOneBody) -> Session:
        session_creator: Session = Session(**body.dict())
        session_creator.id = uuid.uuid4()
        created_session: Session = self.create_one_raw(
            state=state,
            session_creator=session_creator
        )
        return created_session

    def create_one_raw(self, state: State, session_creator: Session) -> Session:
        created_session: Session = self.session_repository.create_one(
            session=state.session,
            session_creator=session_creator
        )
        return created_session

    async def patch_one_by_id(self, state: State, id: UUID, body: PatchOneBody) -> Session:
        session_patcher: Session = Session(**body.dict())
        patched_session: Session = await self.patch_one_by_id_raw(
            state=state,
            id=id,
            session_patcher=session_patcher
        )
        return patched_session

    async def patch_one_by_id_raw(self, state: State, id: UUID, session_patcher: Session) -> Session:
        patched_session: Session = await self.session_repository.patch_one_by_id(
            session=state.session,
            id=id,
            session_patcher=session_patcher
        )
        return patched_session

    async def delete_one_by_id(self, state: State, id: UUID) -> Session:
        deleted_session: Session = await self.session_repository.delete_one_by_id(
            session=state.session,
            id=id
        )
        return deleted_session
