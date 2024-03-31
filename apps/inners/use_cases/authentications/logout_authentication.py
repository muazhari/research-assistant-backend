from starlette.datastructures import State

from apps.inners.models.daos.session import Session
from apps.inners.use_cases.managements.session_management import SessionManagement


class LogoutAuthentication:
    def __init__(
            self,
            session_management: SessionManagement
    ):
        self.session_management = session_management

    async def logout(self, state: State, access_token: str):
        found_session: Session = await self.session_management.find_one_by_access_token(
            state=state,
            access_token=access_token
        )
        await self.session_management.delete_one_by_id(
            state=state,
            id=found_session.id
        )
