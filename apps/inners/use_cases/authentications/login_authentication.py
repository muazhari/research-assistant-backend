import bcrypt
from starlette import status
from starlette.datastructures import State

from apps.inners.models.daos.account import Account
from apps.inners.models.daos.session import Session
from apps.inners.models.dtos.contracts.requests.authentications.logins.login_by_email_and_password_body import \
    LoginByEmailAndPasswordBody
from apps.inners.models.dtos.contracts.responses.authentications.logins.login_response import LoginResponse
from apps.inners.models.dtos.contracts.result import Result
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
            -> Result[LoginResponse]:
        found_account_by_email: Result[Account] = await self.account_management.find_one_by_email(
            state=state,
            email=body.email
        )

        if found_account_by_email.status_code != status.HTTP_200_OK:
            result: Result[LoginResponse] = Result(
                status_code=found_account_by_email.status_code,
                message=f"LoginAuthentication.login_by_email_and_password: Failed, {found_account_by_email.message}",
                data=None
            )
            return result

        is_password_matched: bool = bcrypt.checkpw(
            body.password.encode(),
            found_account_by_email.data.password.encode()
        )
        if not is_password_matched:
            result: Result[LoginResponse] = Result(
                status_code=status.HTTP_401_UNAUTHORIZED,
                message="LoginAuthentication.login_by_email_and_password: Failed, password is not matched.",
                data=None
            )
            return result

        found_session: Result[Session] = await self.session_management.find_one_by_account_id(
            state=state,
            account_id=found_account_by_email.data.id
        )
        if found_session.status_code != status.HTTP_200_OK:
            result: Result[LoginResponse] = Result(
                status_code=found_session.status_code,
                message=f"LoginAuthentication.login_by_email_and_password: Failed, {found_session.message}",
                data=None
            )
            return result

        result: Result[LoginResponse] = Result(
            status_code=status.HTTP_200_OK,
            message="LoginAuthentication.login_by_email_and_password: Succeed.",
            data=LoginResponse(
                account=found_account_by_email.data,
                session=found_session.data
            )
        )
        return result
