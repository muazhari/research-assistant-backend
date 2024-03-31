from typing import Union

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
from apps.inners.use_cases.authentications.login_authentication import LoginAuthentication
from apps.inners.use_cases.authentications.logout_authentication import LogoutAuthentication
from apps.inners.use_cases.authentications.register_authentication import RegisterAuthentication
from apps.outers.containers.application_container import ApplicationContainer
from apps.outers.exceptions import repository_exception, use_case_exception

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
        content: Content[LoginResponse] = Content[LoginResponse](
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=f"{self.__class__.__name__}.{self.login.__name__}: Failed.",
            data=None
        )
        method_param: str = request.query_params.get("method")
        if method_param is None:
            content.status_code = status.HTTP_400_BAD_REQUEST
            content.message += f" {self.__class__.__name__}.{self.login.__name__}: Method is required."
        elif method_param == "email_and_password":
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
            content.message += f" {self.__class__.__name__}.{self.login.__name__}: Method {method_param} is not supported."

        return content.to_response()

    @router.post("/authentications/registers")
    async def register(self, request: Request, body: Union[RegisterByEmailAndPasswordBody]) -> Response:
        content: Content[RegisterResponse] = Content[RegisterResponse](
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=f"{self.__class__.__name__}.{self.register.__name__}: Failed.",
            data=None
        )
        method_param: str = request.query_params.get("method")
        if method_param is None:
            content.status_code = status.HTTP_400_BAD_REQUEST
            content.message += f" {self.__class__.__name__}.{self.register.__name__}: Method is required."
        elif method_param == "email_and_password":
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
            content.message += f" {self.__class__.__name__}.{self.register.__name__}: Method {method_param} is not supported."

        return content.to_response()

    @router.post("/authentications/logouts")
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
