from typing import Any, Union

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from fastapi_utils.cbv import cbv
from starlette import status
from starlette.requests import Request
from starlette.responses import Response

from apps.inners.models.dtos.contracts.content import Content
from apps.inners.models.dtos.contracts.requests.authentications.logins.login_by_email_and_password_body import \
    LoginByEmailAndPasswordBody
from apps.inners.models.dtos.contracts.requests.authentications.registers.register_by_email_and_password_body import \
    RegisterByEmailAndPasswordBody
from apps.inners.models.dtos.contracts.responses.authentications.logins.login_response import LoginResponse
from apps.inners.models.dtos.contracts.responses.authentications.registers.register_response import RegisterResponse
from apps.inners.models.dtos.contracts.result import Result
from apps.inners.use_cases.authentications.login_authentication import LoginAuthentication
from apps.inners.use_cases.authentications.logout_authentication import LogoutAuthentication
from apps.inners.use_cases.authentications.register_authentication import RegisterAuthentication
from apps.outers.containers.application_container import ApplicationContainer

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
            logout_authentication: LogoutAuthentication = Depends(
                Provide[ApplicationContainer.use_cases.authentications.logout]
            )
    ):
        self.login_authentication = login_authentication
        self.register_authentication = register_authentication
        self.logout_authentication = logout_authentication

    @router.post("/authentications/logins")
    async def login(self, request: Request, body: Union[LoginByEmailAndPasswordBody]) -> Response:
        method_param: str = request.query_params.get("method")
        if method_param is None:
            response: Response = Response(
                status_code=status.HTTP_400_BAD_REQUEST,
                content=Content[RegisterResponse](
                    message="AuthenticationController.login: login method is required.",
                    data=None
                ).json()
            )
            return response

        if method_param == "email_and_password":
            result: Result[LoginResponse] = await self.login_authentication.login_by_email_and_password(
                state=request.state,
                body=body
            )
            response: Response = Response(
                status_code=result.status_code,
                content=Content[LoginResponse](
                    message=result.message,
                    data=result.data
                ).json()
            )
        else:
            response: Response = Response(
                status_code=status.HTTP_400_BAD_REQUEST,
                content=Content[LoginResponse](
                    message=f"AuthenticationController.login: login method_param {method_param} is not supported.",
                    data=None
                ).json()
            )
        return response

    @router.post("/authentications/registers")
    async def register(self, request: Request, body: Union[RegisterByEmailAndPasswordBody]) -> Response:
        method_param = request.query_params.get("method")
        if method_param is None:
            response: Response = Response(
                status_code=status.HTTP_400_BAD_REQUEST,
                content=Content[RegisterResponse](
                    message="AuthenticationController.register: register method is required.",
                    data=None
                ).json()
            )
            return response

        if method_param == "email_and_password":
            result: Result[RegisterResponse] = await self.register_authentication.register_by_email_and_password(
                state=request.state,
                body=body
            )
            response: Response = Response(
                status_code=result.status_code,
                content=Content[RegisterResponse](
                    message=result.message,
                    data=result.data
                ).json()
            )
        else:
            response: Response = Response(
                status_code=status.HTTP_400_BAD_REQUEST,
                content=Content[RegisterResponse](
                    message=f"AuthenticationController.register: register method_param {method_param} is not supported.",
                    data=None
                ).json()
            )
        return response

    @router.post("/authentications/logouts")
    async def logout(self, request: Request) -> Response:
        access_token: str = request.headers.get("Authorization").split(" ")[1]
        result: Result[Any] = await self.logout_authentication.logout(
            state=request.state,
            access_token=access_token
        )
        response: Response = Response(
            status_code=result.status_code,
            content=Content[Any](
                message=result.message,
                data=result.data
            ).json()
        )
        return response
