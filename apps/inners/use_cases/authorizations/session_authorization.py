import uuid
from datetime import datetime, timedelta, timezone

from starlette.datastructures import State

from apps.inners.models.daos.session import Session
from apps.inners.models.dtos.contracts.requests.authorizations.refresh_access_token_body import RefreshAccessTokenBody
from apps.inners.use_cases.managements.account_management import AccountManagement
from apps.inners.use_cases.managements.session_management import SessionManagement


class SessionAuthorization:
    def __init__(
            self,
            session_management: SessionManagement,
            account_management: AccountManagement
    ):
        self.session_management = session_management
        self.account_management = account_management

    async def refresh_access_token(self, state: State, body: RefreshAccessTokenBody) -> Session:
        found_session: Session = await self.session_management.find_one_by_refresh_token(
            state=state,
            refresh_token=body.refresh_token
        )

        current_time = datetime.now(tz=timezone.utc)
        found_session.access_token = str(uuid.uuid4())
        found_session.access_token_expired_at = current_time + timedelta(minutes=15)

        patched_session: Session = await self.session_management.patch_one_by_id_raw(
            state=state,
            id=found_session.id,
            session_patcher=found_session
        )
        return patched_session
