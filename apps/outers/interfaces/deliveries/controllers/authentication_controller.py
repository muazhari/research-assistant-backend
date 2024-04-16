from typing import Union

from fastapi import APIRouter
from starlette import status
from starlette.requests import Request
from starlette.responses import Response

from apps.inners.exceptions import repository_exception
from apps.inners.exceptions import use_case_exception
from apps.inners.models.dtos.content import Content
from apps.inners.models.dtos.contracts.requests.authentications.logins.login_by_email_and_password_body import \
    LoginByEmailAndPasswordBody
from apps.inners.models.dtos.contracts.requests.authentications.registers.register_by_email_and_password_body import \
    RegisterByEmailAndPasswordBody
from apps.inners.models.dtos.contracts.responses.authentications.logins.login_response import LoginResponse
from apps.inners.models.dtos.contracts.responses.authentications.registers.register_response import RegisterResponse
from apps.inners.use_cases.authentications.login_authentication import LoginAuthentication
from apps.inners.use_cases.authentications.logout_authentication import LogoutAuthentication
from apps.inners.use_cases.authentications.register_authentication import RegisterAuthentication


class AuthenticationController:

    def __init__(
            self,
            login_authentication: LoginAuthentication,
            register_authentication: RegisterAuthentication,
            logout_authentication: LogoutAuthentication
    ):
        self.router: APIRouter = APIRouter(
            tags=["authentications"],
            prefix="/authentications",
        )
        self.router.add_api_route(
            path="/logins",
            endpoint=self.login,
            methods=["POST"]
        )
        self.router.add_api_route(
            path="/registers",
            endpoint=self.register,
            methods=["POST"]
        )
        self.router.add_api_route(
            path="/logouts",
            endpoint=self.logout,
            methods=["POST"]
        )
        self.login_authentication = login_authentication
        self.register_authentication = register_authentication
        self.logout_authentication = logout_authentication

    async def login(self, request: Request, body: Union[LoginByEmailAndPasswordBody], method: str) -> Response:
        content: Content[LoginResponse] = Content[LoginResponse](
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=f"{self.__class__.__name__}.{self.login.__name__}: Failed.",
            data=None
        )

        if method == "email_and_password":
            try:
                data: LoginResponse = await self.login_authentication.login_by_email_and_password(
                    state=request.state,
                    body=body
                )
                content.status_code = status.HTTP_200_OK
                content.message = f"{self.__class__.__name__}.{self.login.__name__}: Succeed."
                content.data = data
            except use_case_exception.PasswordNotMatched as exception:
                content.status_code = status.HTTP_401_UNAUTHORIZED
                content.message += f" {exception.caller.class_name}.{exception.caller.function_name}: {exception.__class__.__name__}."
            except repository_exception.NotFound as exception:
                content.status_code = status.HTTP_404_NOT_FOUND
                content.message += f" {exception.caller.class_name}.{exception.caller.function_name}: {exception.__class__.__name__}."
        else:
            content.status_code = status.HTTP_400_BAD_REQUEST
            content.message += f" {self.__class__.__name__}.{self.login.__name__}: Method {method} is not supported."

        return content.to_response()

    async def register(self, request: Request, body: Union[RegisterByEmailAndPasswordBody], method: str) -> Response:
        content: Content[RegisterResponse] = Content[RegisterResponse](
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=f"{self.__class__.__name__}.{self.register.__name__}: Failed.",
            data=None
        )

        if method == "email_and_password":
            try:
                data: RegisterResponse = await self.register_authentication.register_by_email_and_password(
                    state=request.state,
                    body=body
                )
                content.status_code = status.HTTP_201_CREATED
                content.message = f"{self.__class__.__name__}.{self.register.__name__}: Succeed."
                content.data = data
            except use_case_exception.EmailAlreadyExists as exception:
                content.status_code = status.HTTP_409_CONFLICT
                content.message += f" {exception.caller.class_name}.{exception.caller.function_name}: {exception.__class__.__name__}."
            except repository_exception.IntegrityError as exception:
                content.status_code = status.HTTP_409_CONFLICT
                content.message += f" {exception.caller.class_name}.{exception.caller.function_name}: {exception.__class__.__name__}."
            except repository_exception.NotFound as exception:
                content.status_code = status.HTTP_404_NOT_FOUND
                content.message += f" {exception.caller.class_name}.{exception.caller.function_name}: {exception.__class__.__name__}."
        else:
            content.status_code = status.HTTP_400_BAD_REQUEST
            content.message += f" {self.__class__.__name__}.{self.register.__name__}: Method {method} is not supported."

        return content.to_response()

    async def logout(self, request: Request) -> Response:
        content: Content[RegisterResponse] = Content[RegisterResponse](
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=f"{self.__class__.__name__}.{self.logout.__name__}: Failed.",
            data=None
        )
        access_token: str = request.headers.get("Authorization").split(" ")[1]
        try:
            await self.logout_authentication.logout(
                state=request.state,
                access_token=access_token
            )
            content.status_code = status.HTTP_200_OK
            content.message = f"{self.__class__.__name__}.{self.logout.__name__}: Succeed."
        except repository_exception.NotFound as exception:
            content.status_code = status.HTTP_404_NOT_FOUND
            content.message += f" {exception.caller.class_name}.{exception.caller.function_name}: {exception.__class__.__name__}."

        return content.to_response()
