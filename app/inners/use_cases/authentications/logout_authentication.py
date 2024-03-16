from typing import Any

from sqlmodel.ext.asyncio.session import AsyncSession
from starlette import status

from app.inners.models.daos.session import Session
from app.inners.models.dtos.contracts.result import Result
from app.inners.use_cases.managements.session_management import SessionManagement


class LogoutAuthentication:
    def __init__(
            self,
            session_management: SessionManagement
    ):
        self.session_management = session_management

    async def logout(self, session: AsyncSession, access_token: str) -> Result[Any]:
        found_session: Result[Session] = await self.session_management.find_one_by_access_token(
            session=session,
            access_token=access_token
        )

        if found_session.status_code != status.HTTP_200_OK:
            result: Result[Any] = Result(
                status_code=found_session.status_code,
                message=f"LogoutAuthentication.logout: Failed, {found_session.message}",
                data=None
            )
            return result

        deleted_session: Result[Session] = await self.session_management.delete_one_by_id(
            session=session,
            id=found_session.data.id
        )

        if deleted_session.status_code != status.HTTP_200_OK:
            result: Result[Any] = Result(
                status_code=deleted_session.status_code,
                message=f"LogoutAuthentication.logout: Failed, {deleted_session.message}",
                data=None
            )
            return result

        result: Result[Any] = Result(
            status_code=status.HTTP_200_OK,
            message="LogoutAuthentication.logout: Succeed.",
            data=None
        )
        return result
