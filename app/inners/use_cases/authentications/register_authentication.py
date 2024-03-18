from starlette import status
from starlette.datastructures import State

from app.inners.models.daos.account import Account
from app.inners.models.dtos.contracts.requests.authentications.registers.register_by_email_and_password_body import \
    RegisterByEmailAndPasswordBody
from app.inners.models.dtos.contracts.requests.managements.accounts.create_one_body import CreateOneBody
from app.inners.models.dtos.contracts.responses.authentications.registers.register_response import \
    RegisterResponse
from app.inners.models.dtos.contracts.result import Result
from app.inners.use_cases.managements.account_management import AccountManagement
from app.outers.interfaces.deliveries.middlewares.session_middleware import SessionMiddleware


class RegisterAuthentication:
    def __init__(
            self,
            account_management: AccountManagement
    ):
        self.account_management = account_management

    async def register_by_email_and_password(
            self,
            state: State,
            body: RegisterByEmailAndPasswordBody
    ) -> Result[RegisterResponse]:
        found_account_by_email: Result[Account] = await self.account_management.find_one_by_email(
            state=state,
            email=body.email
        )

        if found_account_by_email.status_code == status.HTTP_200_OK:
            result: Result[RegisterResponse] = Result(
                status_code=status.HTTP_409_CONFLICT,
                message="RegisterAuthentication.register_by_email_and_password: Failed, email is already used.",
                data=None
            )
            return result

        account_to_create_body: CreateOneBody = CreateOneBody(
            email=body.email,
            password=body.password
        )
        created_account: Result[Account] = await self.account_management.create_one(
            state=state,
            body=account_to_create_body
        )

        if created_account.status_code != status.HTTP_201_CREATED:
            result: Result[RegisterResponse] = Result(
                status_code=created_account.status_code,
                message=f"RegisterAuthentication.register_by_email_and_password: Failed, {created_account.message}",
                data=None
            )
            raise SessionMiddleware.HandlerException(
                result=result
            )

        register_response: RegisterResponse = RegisterResponse(
            account=created_account.data
        )
        result: Result[RegisterResponse] = Result(
            status_code=status.HTTP_201_CREATED,
            message="RegisterAuthentication.register_by_email_and_password: Succeed.",
            data=register_response
        )
        return result
