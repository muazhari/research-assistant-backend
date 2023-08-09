from app.inners.models.entities.account import Account
from app.inners.models.value_objects.contracts.requests.authentications.logins.login_by_email_and_password_request import \
    LoginByEmailAndPasswordRequest
from app.inners.models.value_objects.contracts.responses.authentications.logins.login_response import LoginResponse
from app.inners.models.value_objects.contracts.responses.content import Content
from app.inners.use_cases.managements.account_management import AccountManagement


class LoginAuthentication:
    def __init__(
            self,
            account_management: AccountManagement
    ):
        self.account_management = account_management

    async def login_by_email_and_password(self, request: LoginByEmailAndPasswordRequest) -> Content[LoginResponse]:
        found_account_by_email: Content[Account] = await self.account_management.read_one_by_email(request.body.email)
        found_account_by_email_and_password: Content[
            Account] = await self.account_management.read_one_by_email_and_password(
            request.body.email,
            request.body.password)

        if found_account_by_email.data is None:
            content: Content[LoginResponse] = Content[LoginResponse](
                data=None,
                message="Authentication login failed: Email not found."
            )
            return content

        if found_account_by_email_and_password.data is None:
            content: Content[LoginResponse] = Content[LoginResponse](
                data=None,
                message="Authentication login failed: Wrong password."
            )
            return content

        content: Content[LoginResponse] = Content[LoginResponse](
            data=LoginResponse(
                account=found_account_by_email_and_password.data
            ),
            message="Authentication login succeed."
        )

        return content
