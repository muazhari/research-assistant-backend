from datetime import datetime

from sqlalchemy.engine import Result
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette import status
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from apps.inners.models.daos.session import Session
from apps.inners.models.dtos.contracts.content import Content


class AuthorizationMiddleware(BaseHTTPMiddleware):
    def __init__(
            self,
            app
    ):
        super().__init__(app)
        pass

    async def dispatch(
            self,
            request: Request,
            call_next: RequestResponseEndpoint
    ) -> Response:
        session: AsyncSession = request.state.session

        authorization_header = request.headers.get("Authorization")
        if not authorization_header:
            response: Response = Response(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content=Content(
                    message="AuthorizationMiddleware.dispatch: Authorization header is missing.",
                    data=None
                ).json()
            )
            return response

        access_token = authorization_header.split(" ")[1]

        found_session_result: Result = await session.execute(
            select(Session).where(Session.access_token == access_token).limit(1)
        )
        found_sessions: [Session] = found_session_result.scalars().all()
        if len(found_sessions) == 0:
            response: Response = Response(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content=Content(
                    message="AuthorizationMiddleware.dispatch: Session is not found by access token.",
                    data=None
                ).json()
            )
            return response

        found_session: Session = found_sessions[0]

        if found_session.access_token_expired_at < datetime.now(tz=timezone.utc):
            response: Response = Response(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content=Content(
                    message="AuthorizationMiddleware.dispatch: Session is expired.",
                    data=None
                ).json()
            )
            return response

        request.state.authorized_session = found_session
        response: Response = await call_next(request)
        return response
