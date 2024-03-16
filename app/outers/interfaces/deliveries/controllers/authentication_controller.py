from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from fastapi_utils.cbv import cbv
from starlette import status
from starlette.requests import Request
from starlette.responses import Response

from app.inners.models.dtos.contracts.content import Content
from app.inners.models.dtos.contracts.requests.authentications.logins.login_by_email_and_password_body import \
    LoginByEmailAndPasswordBody
from app.inners.models.dtos.contracts.requests.authentications.registers.register_by_email_and_password_body import \
    RegisterByEmailAndPasswordBody
from app.inners.models.dtos.contracts.responses.authentications.logins.login_response import LoginResponse
from app.inners.models.dtos.contracts.responses.authentications.registers.register_response import RegisterResponse
from app.inners.models.dtos.contracts.result import Result
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

    @router.post("/authentications/logins")
    async def login(self, request: Request, body: LoginByEmailAndPasswordBody) -> Response:
        method: str = request.query_params.get("method")
        if method is None:
            response: Response = Response(
                status_code=status.HTTP_400_BAD_REQUEST,
                content=Content[RegisterResponse](
                    message="AuthenticationController.login: login method is required.",
                    data=None
                )
            )
            return response

        if method == "email_and_password":
            result: Result[LoginResponse] = await self.login_authentication.login_by_email_and_password(
                session=request.state.session,
                body=body
            )
            response: Response = Response(
                status_code=result.status_code,
                content=Content[LoginResponse](
                    message=result.message,
                    data=result.data
                )
            )
        else:
            response: Response = Response(
                status_code=status.HTTP_400_BAD_REQUEST,
                content=Content[LoginResponse](
                    message=f"AuthenticationController.login: login method {method} is not supported.",
                    data=None
                )
            )
        return response

    @router.post("/authentications/registers")
    async def register(self, request: Request, body: RegisterByEmailAndPasswordBody) -> Response:
        method = request.query_params.get("method")
        if method is None:
            response: Response = Response(
                status_code=status.HTTP_400_BAD_REQUEST,
                content=Content[RegisterResponse](
                    message="AuthenticationController.register: register method is required.",
                    data=None
                )
            )
            return response

        if method == "email_and_password":
            result: Result[RegisterResponse] = await self.register_authentication.register_by_email_and_password(
                session=request.state.session,
                body=body
            )
            response: Response = Response(
                status_code=result.status_code,
                content=Content[RegisterResponse](
                    message=result.message,
                    data=result.data
                )
            )
        else:
            response: Response = Response(
                status_code=status.HTTP_400_BAD_REQUEST,
                content=Content[RegisterResponse](
                    message=f"AuthenticationController.register: register method {method} is not supported.",
                    data=None
                )
            )
        return response
