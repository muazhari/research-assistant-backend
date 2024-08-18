from datetime import datetime, timezone
from typing import List

import regex
from starlette import status
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from apps.inners.exceptions import repository_exception
from apps.inners.models.daos.session import Session
from apps.inners.models.dtos.content import Content
from apps.inners.use_cases.managements.session_management import SessionManagement


class AuthorizationMiddleware(BaseHTTPMiddleware):
    def __init__(
            self,
            app,
            session_management: SessionManagement
    ):
        super().__init__(app)
        self.session_management: SessionManagement = session_management
        self.unauthorized_path_patterns = [
            r".*\/docs.*",
            r".*\/openapi.json.*",
            r".*\/authentications\/logins.*",
            r".*\/authentications\/registers.*",
            r".*\/authorizations\/refreshes.*"
        ]

    def is_unauthorized_path(self, path: str) -> bool:
        pattern: str = "|".join(self.unauthorized_path_patterns)
        return regex.match(pattern, path) is not None

    async def dispatch(
            self,
            request: Request,
            call_next: RequestResponseEndpoint
    ) -> Response:
        content: Content[Session] = Content(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=f"{self.__class__.__name__}.{self.dispatch.__name__}: Failed.",
            data=None
        )

        if self.is_unauthorized_path(request.url.path):
            response: Response = await call_next(request)
            return response

        authorization_header = request.headers.get("Authorization")
        if not authorization_header:
            content.status_code = status.HTTP_401_UNAUTHORIZED
            content.message += f" {self.__class__.__name__}.{self.dispatch.__name__}: Authorization header is missing."
            return content.to_response()

        authorization: List[str] = authorization_header.split(" ")

        if len(authorization) != 2:
            content.status_code = status.HTTP_401_UNAUTHORIZED
            content.message += f" {self.__class__.__name__}.{self.dispatch.__name__}: Authorization is invalid."
            return content.to_response()

        if authorization[0] != "Bearer":
            content.status_code = status.HTTP_401_UNAUTHORIZED
            content.message += f" {self.__class__.__name__}.{self.dispatch.__name__}: Authorization scheme is invalid."
            return content.to_response()

        access_token: str = authorization[1]

        try:
            found_session: [Session] = await self.session_management.find_one_by_access_token(
                state=request.state,
                access_token=access_token
            )
        except repository_exception.NotFound as exception:
            content.status_code = status.HTTP_404_NOT_FOUND
            content.message += f" {exception.caller.class_name}.{exception.caller.function_name}: {exception.__class__.__name__}"
            return content.to_response()

        if found_session.access_token_expired_at < datetime.now(tz=timezone.utc):
            content.status_code = status.HTTP_401_UNAUTHORIZED
            content.message += f" {self.__class__.__name__}.{self.dispatch.__name__}: Access token is expired."
            return content.to_response()

        request.state.authorized_session = found_session
        response: Response = await call_next(request)

        return response
