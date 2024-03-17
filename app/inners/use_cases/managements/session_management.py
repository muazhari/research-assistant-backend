from uuid import UUID

from sqlalchemy import exc
from starlette import status
from starlette.datastructures import State

from app.inners.models.daos.session import Session
from app.inners.models.dtos.contracts.requests.managements.sessions.create_one_body import CreateOneBody
from app.inners.models.dtos.contracts.requests.managements.sessions.patch_one_body import PatchOneBody
from app.inners.models.dtos.contracts.result import Result
from app.outers.repositories.session_repository import SessionRepository


class SessionManagement:
    def __init__(
            self,
            session_repository: SessionRepository,
    ):
        self.session_repository: SessionRepository = session_repository

    async def find_one_by_id(self, state: State, id: UUID) -> Result[Session]:
        try:
            found_session: Session = await self.session_repository.find_one_by_id(
                session=state.session,
                id=id
            )
            result: Result[Session] = Result(
                status_code=status.HTTP_200_OK,
                message="SessionManagement.find_one_by_id: Succeed.",
                data=found_session,
            )
        except exc.NoResultFound:
            result: Result[Session] = Result(
                status_code=status.HTTP_404_NOT_FOUND,
                message="SessionManagement.find_one_by_id: Failed, session is not found.",
                data=None,
            )
        return result

    async def find_one_by_account_id(self, state: State, account_id: UUID) -> Result[Session]:
        try:
            found_session: Session = await self.session_repository.find_one_by_account_id(
                session=state.session,
                account_id=account_id
            )
            result: Result[Session] = Result(
                status_code=status.HTTP_200_OK,
                message="SessionManagement.find_one_by_account_id: Succeed.",
                data=found_session,
            )
        except exc.NoResultFound:
            result: Result[Session] = Result(
                status_code=status.HTTP_404_NOT_FOUND,
                message="SessionManagement.find_one_by_account_id: Failed, session is not found.",
                data=None,
            )
        return result

    async def find_one_by_access_token(self, state: State, access_token: str) -> Result[Session]:
        try:
            found_session: Session = await self.session_repository.find_one_by_access_token(
                session=state.session,
                access_token=access_token
            )
            result: Result[Session] = Result(
                status_code=status.HTTP_200_OK,
                message="SessionManagement.find_one_by_access_token: Succeed.",
                data=found_session,
            )
        except exc.NoResultFound:
            result: Result[Session] = Result(
                status_code=status.HTTP_404_NOT_FOUND,
                message="SessionManagement.find_one_by_access_token: Failed, session is not found.",
                data=None,
            )
        return result

    async def find_one_by_refresh_token(self, state: State, refresh_token: str) -> Result[Session]:
        try:
            found_session: Session = await self.session_repository.find_one_by_refresh_token(
                session=state.session,
                refresh_token=refresh_token
            )
            result: Result[Session] = Result(
                status_code=status.HTTP_200_OK,
                message="SessionManagement.find_one_by_refresh_token: Succeed.",
                data=found_session,
            )
        except exc.NoResultFound:
            result: Result[Session] = Result(
                status_code=status.HTTP_404_NOT_FOUND,
                message="SessionManagement.find_one_by_refresh_token: Failed, session is not found.",
                data=None,
            )
        return result

    async def create_one(self, state: State, body: CreateOneBody) -> Result[Session]:
        session_to_create: Session = Session(**body.dict())
        created_session: Session = await self.session_repository.create_one(
            session=state.session,
            session_to_create=session_to_create
        )
        result: Result[Session] = Result(
            status_code=status.HTTP_201_CREATED,
            message="SessionManagement.create_one: Succeed.",
            data=created_session,
        )
        return result

    async def create_one_raw(self, state: State, session_to_create: Session) -> Result[Session]:
        created_session: Session = await self.session_repository.create_one(
            session=state.session,
            session_to_create=session_to_create
        )
        result: Result[Session] = Result(
            status_code=status.HTTP_201_CREATED,
            message="SessionManagement.create_one_raw: Succeed.",
            data=created_session,
        )
        return result

    async def patch_one_by_id(self, state: State, id: UUID, body: PatchOneBody) -> Result[Session]:
        try:
            session_to_patch: Session = Session(**body.dict())
            patched_session: Session = await self.session_repository.patch_one_by_id(
                session=state.session,
                id=id,
                session_to_patch=session_to_patch
            )
            result: Result[Session] = Result(
                status_code=status.HTTP_200_OK,
                message="SessionManagement.patch_one_by_id: Succeed.",
                data=patched_session,
            )
        except exc.NoResultFound:
            result: Result[Session] = Result(
                status_code=status.HTTP_404_NOT_FOUND,
                message="SessionManagement.patch_one_by_id: Failed, session is not found.",
                data=None,
            )
        return result

    async def patch_one_by_id_raw(self, state: State, id: UUID, session_to_patch: Session) -> Result[Session]:
        try:
            patched_session: Session = await self.session_repository.patch_one_by_id(
                session=state.session,
                id=id,
                session_to_patch=session_to_patch
            )
            result: Result[Session] = Result(
                status_code=status.HTTP_200_OK,
                message="SessionManagement.patch_one_by_id_raw: Succeed.",
                data=patched_session,
            )
        except exc.NoResultFound:
            result: Result[Session] = Result(
                status_code=status.HTTP_404_NOT_FOUND,
                message="SessionManagement.patch_one_by_id_raw: Failed, session is not found.",
                data=None,
            )
        return result

    async def delete_one_by_id(self, state: State, id: UUID) -> Result[Session]:
        try:
            deleted_session: Session = await self.session_repository.delete_one_by_id(
                session=state.session,
                id=id
            )
            result: Result[Session] = Result(
                status_code=status.HTTP_200_OK,
                message="SessionManagement.delete_one_by_id: Succeed.",
                data=deleted_session,
            )
        except exc.NoResultFound:
            result: Result[Session] = Result(
                status_code=status.HTTP_404_NOT_FOUND,
                message="SessionManagement.delete_one_by_id: Failed, session is not found.",
                data=None,
            )
        return result
