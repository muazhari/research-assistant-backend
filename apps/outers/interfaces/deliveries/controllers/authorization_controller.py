from typing import Union

from fastapi import APIRouter
from starlette import status
from starlette.requests import Request
from starlette.responses import Response

from apps.inners.exceptions import repository_exception
from apps.inners.models.daos.session import Session
from apps.inners.models.dtos.content import Content
from apps.inners.models.dtos.contracts.requests.authorizations.refresh_access_token_body import RefreshAccessTokenBody
from apps.inners.use_cases.authorizations.session_authorization import SessionAuthorization


class AuthorizationController:

    def __init__(
            self,
            session_authorization: SessionAuthorization
    ):
        self.router: APIRouter = APIRouter(
            tags=["authorizations"],
            prefix="/authorizations"
        )
        self.router.add_api_route(
            path="/refreshes",
            endpoint=self.refresh,
            methods=["POST"]
        )
        self.session_authorization = session_authorization

    async def refresh(self, request: Request, body: Union[RefreshAccessTokenBody], token_type: str) -> Response:
        content: Content[Session] = Content[Session](
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=f"{self.__class__.__name__}.{self.refresh.__name__}: Failed.",
            data=None
        )

        if token_type is None:
            content.status_code = status.HTTP_400_BAD_REQUEST
            content.message += f" {self.__class__.__name__}.{self.refresh.__name__}: Type is required."
        elif token_type == "access-token":
            try:
                data: Session = await self.session_authorization.refresh_access_token(
                    state=request.state,
                    body=body
                )
                content.status_code = status.HTTP_200_OK
                content.message = f"{self.__class__.__name__}.{self.refresh.__name__}: Succeed."
                content.data = data
            except repository_exception.NotFound as exception:
                content.status_code = status.HTTP_404_NOT_FOUND
                content.message += f" {exception.__class__.__name__}."
        else:
            content.status_code = status.HTTP_400_BAD_REQUEST
            content.message += f" {self.__class__.__name__}.{self.refresh.__name__}: Invalid type."

        return content.to_response()
