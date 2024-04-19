import uuid
from datetime import datetime, timezone, timedelta

import bcrypt
from starlette.datastructures import State

from apps.inners.exceptions import repository_exception
from apps.inners.exceptions import use_case_exception
from apps.inners.models.daos.account import Account
from apps.inners.models.daos.session import Session
from apps.inners.models.dtos.contracts.requests.authentications.logins.login_by_email_and_password_body import \
    LoginByEmailAndPasswordBody
from apps.inners.models.dtos.contracts.responses.authentications.logins.login_response import LoginResponse
from apps.inners.use_cases.managements.account_management import AccountManagement
from apps.inners.use_cases.managements.session_management import SessionManagement


class LoginAuthentication:
    def __init__(
            self,
            account_management: AccountManagement,
            session_management: SessionManagement
    ):
        self.account_management = account_management
        self.session_management = session_management

    async def login_by_email_and_password(self, state: State, body: LoginByEmailAndPasswordBody) \
            -> LoginResponse:
        found_account_by_email: Account = await self.account_management.find_one_by_email(
            state=state,
            email=body.email
        )
        is_password_matched: bool = bcrypt.checkpw(
            body.password.encode(),
            found_account_by_email.password.encode()
        )
        if not is_password_matched:
            raise use_case_exception.PasswordNotMatched()

        try:
            found_session: Session = await self.session_management.find_one_by_account_id(
                state=state,
                account_id=found_account_by_email.id
            )
            current_session: Session = found_session
        except repository_exception.NotFound:
            current_time = datetime.now(tz=timezone.utc)
            session_creator: Session = Session(
                id=uuid.uuid4(),
                account_id=found_account_by_email.id,
                access_token=str(uuid.uuid4()),
                refresh_token=str(uuid.uuid4()),
                access_token_expired_at=current_time + timedelta(minutes=10),
                refresh_token_expired_at=current_time + timedelta(days=7),
            )
            created_session: Session = self.session_management.create_one_raw(
                state=state,
                session_creator=session_creator
            )
            current_session: Session = created_session

        login_response: LoginResponse = LoginResponse(
            account=found_account_by_email,
            session=current_session
        )
        return login_response
