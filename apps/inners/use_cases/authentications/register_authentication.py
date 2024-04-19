from starlette.datastructures import State

from apps.inners.exceptions import repository_exception
from apps.inners.exceptions import use_case_exception
from apps.inners.models.daos.account import Account
from apps.inners.models.dtos.contracts.requests.authentications.registers.register_by_email_and_password_body import \
    RegisterByEmailAndPasswordBody
from apps.inners.models.dtos.contracts.requests.managements.accounts.create_one_body import CreateOneBody
from apps.inners.models.dtos.contracts.responses.authentications.registers.register_response import \
    RegisterResponse
from apps.inners.use_cases.managements.account_management import AccountManagement


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
    ) -> RegisterResponse:
        try:
            await self.account_management.find_one_by_email(
                state=state,
                email=body.email
            )
        except repository_exception.NotFound:
            pass
        else:
            raise use_case_exception.EmailAlreadyExists()

        account_creator_body: CreateOneBody = CreateOneBody(
            email=body.email,
            password=body.password
        )
        created_account: Account = await self.account_management.create_one(
            state=state,
            body=account_creator_body
        )
        register_response: RegisterResponse = RegisterResponse(
            account=created_account
        )
        return register_response
