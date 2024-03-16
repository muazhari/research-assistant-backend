import bcrypt
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette import status

from app.inners.models.daos.account import Account
from app.inners.models.dtos.contracts.requests.authentications.logins.login_by_email_and_password_body import \
    LoginByEmailAndPasswordBody
from app.inners.models.dtos.contracts.responses.authentications.logins.login_response import LoginResponse
from app.inners.models.dtos.contracts.result import Result
from app.inners.use_cases.managements.account_management import AccountManagement


class LoginAuthentication:
    def __init__(
            self,
            account_management: AccountManagement
    ):
        self.account_management = account_management

    async def login_by_email_and_password(self, session: AsyncSession, body: LoginByEmailAndPasswordBody) \
            -> Result[LoginResponse]:
        found_account_by_email: Result[Account] = await self.account_management.find_one_by_email(
            session=session,
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

        found_session

        return result
