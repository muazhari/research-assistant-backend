from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from fastapi_utils.cbv import cbv

from app.inners.models.value_objects.contracts.requests.authentications.logins.login_by_email_and_password_body import \
    LoginByEmailAndPasswordBody
from app.inners.models.value_objects.contracts.requests.authentications.logins.login_by_email_and_password_request import \
    LoginByEmailAndPasswordRequest
from app.inners.models.value_objects.contracts.requests.authentications.registers.register_by_email_and_password_body import \
    RegisterByEmailAndPasswordBody
from app.inners.models.value_objects.contracts.requests.authentications.registers.register_by_email_and_password_request import \
    RegisterByEmailAndPasswordRequest
from app.inners.models.value_objects.contracts.responses.authentications.logins.login_response import LoginResponse
from app.inners.models.value_objects.contracts.responses.authentications.registers.register_response import \
    RegisterResponse
from app.inners.models.value_objects.contracts.responses.content import Content
from app.inners.use_cases.authentications.login_authentication import LoginAuthentication
from app.inners.use_cases.authentications.register_authentication import RegisterAuthentication
from app.outers.containers.application_container import ApplicationContainer

router: APIRouter = APIRouter(tags=["authentications"])


@cbv(router)
class AuthenticationController:

    @inject
    def __init__(
            self,
            login_authentication: LoginAuthentication = Depends(
                Provide[ApplicationContainer.use_cases.authentications.login]
            ),
            register_authentication: RegisterAuthentication = Depends(
                Provide[ApplicationContainer.use_cases.authentications.register]
            ),
    ):
        self.login_authentication = login_authentication
        self.register_authentication = register_authentication

    @router.post("/authentications/logins/email-and-password")
    async def login(self, body: LoginByEmailAndPasswordBody) -> Content[LoginResponse]:
        request: LoginByEmailAndPasswordRequest = LoginByEmailAndPasswordRequest(
            body=body
        )
        return await self.login_authentication.login_by_email_and_password(request)

    @router.post("/authentications/registers/email-and-password")
    async def register(self, body: RegisterByEmailAndPasswordBody) -> Content[RegisterResponse]:
        request: RegisterByEmailAndPasswordRequest = RegisterByEmailAndPasswordRequest(
            body=body
        )
        return await self.register_authentication.register_by_email_and_password(request)
