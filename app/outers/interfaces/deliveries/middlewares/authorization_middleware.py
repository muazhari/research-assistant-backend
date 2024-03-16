from datetime import datetime

from dependency_injector.wiring import inject
from sqlmodel import select
from sqlmodel.engine.result import Result
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette import status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from app.inners.models.daos.session import Session
from app.inners.models.dtos.contracts.content import Content
from app.outers.datastores.one_datastore import OneDatastore


class AuthorizationMiddleware(BaseHTTPMiddleware):
    @inject
    def __init__(
            self,
            app,
            one_datastore: OneDatastore
    ):
        super().__init__(app)
        self.one_datastore = one_datastore

    async def dispatch(self, request, call_next):
        session: AsyncSession = request.state.session

        authorization_header = request.headers.get("Authorization")
        if not authorization_header:
            response: Response = Response(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content=Content(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    message="AuthorizationMiddleware.dispatch: Authorization header is missing.",
                    data=None
                )
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
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    message="AuthorizationMiddleware.dispatch: Session is not found by access token.",
                    data=None
                )
            )
            return response

        found_session: Session = found_sessions[0]

        if found_session.access_token_expired_at < datetime.now():
            response: Response = Response(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content=Content(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    message="AuthorizationMiddleware.dispatch: Session is expired.",
                    data=None
                )
            )
            return response

        request.state.authorized_session = found_session
        response: Response = await call_next(request)
        return response
