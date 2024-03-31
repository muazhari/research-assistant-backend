from sqlmodel.ext.asyncio.session import AsyncSession
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp

from apps.outers.datastores.one_datastore import OneDatastore


class SessionMiddleware(BaseHTTPMiddleware):
    def __init__(
            self,
            app: ASGIApp,
            one_datastore: OneDatastore
    ):
        super().__init__(app)
        self.one_datastore = one_datastore

    async def dispatch(
            self,
            request: Request,
            call_next: RequestResponseEndpoint
    ) -> Response:
        async def handler(session: AsyncSession):
            request.state.session = session
            handler_response: Response = await call_next(request)
            return handler_response

        response: Response = await self.one_datastore.retryable(handler)
        return response
