import uuid
from datetime import datetime, timedelta, timezone

from starlette import status
from starlette.datastructures import State

from app.inners.models.daos.session import Session
from app.inners.models.dtos.contracts.requests.authorizations.refresh_access_token_body import RefreshAccessTokenBody
from app.inners.models.dtos.contracts.result import Result
from app.inners.use_cases.managements.account_management import AccountManagement
from app.inners.use_cases.managements.session_management import SessionManagement


class SessionAuthorization:
    def __init__(
            self,
            session_management: SessionManagement,
            account_management: AccountManagement
    ):
        self.session_management = session_management
        self.account_management = account_management

    async def refresh_access_token(self, state: State, body: RefreshAccessTokenBody) -> Result[Session]:
        found_session: Result[Session] = await self.session_management.find_one_by_refresh_token(
            state=state,
            refresh_token=body.refresh_token
        )

        if found_session.status_code != status.HTTP_200_OK:
            result: Result[Session] = Result(
                status_code=found_session.status_code,
                message=f"SessionAuthorization.refresh_access_token: Failed, {found_session.message}",
                data=None
            )
            return result

        current_time = datetime.now(tz=timezone.utc)
        found_session.data.access_token = str(uuid.uuid4())
        found_session.data.access_token_expired_at = current_time + timedelta(minutes=15)

        patched_session: Result[Session] = await self.session_management.patch_one_by_id_raw(
            state=state,
            id=found_session.data.id,
            session_patcher=found_session.data
        )
        if patched_session.status_code != status.HTTP_200_OK:
            result: Result[Session] = Result(
                status_code=patched_session.status_code,
                message=f"SessionAuthorization.refresh_access_token: Failed, {patched_session.message}",
                data=None
            )
            return result

        result: Result[Session] = Result(
            status_code=status.HTTP_200_OK,
            message="SessionAuthorization.refresh_access_token: Succeed.",
            data=found_session.data
        )
        return result
