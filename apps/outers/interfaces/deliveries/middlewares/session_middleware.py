from sqlmodel.ext.asyncio.session import AsyncSession
from starlette import status
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp

from apps.inners.exceptions import datastore_exception
from apps.inners.models.dtos.content import Content
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
        content: Content = Content(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=f"{self.__class__.__name__}.{self.dispatch.__name__}: Failed.",
            data=None
        )

        async def handler(session: AsyncSession):
            request.state.session = session
            handler_response: Response = await call_next(request)

            return handler_response

        try:
            response: Response = await self.one_datastore.retryable(handler)
        except datastore_exception.MaxRetriesExceeded as exception:
            content.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            content.message += f" {exception.caller.class_name}.{exception.caller.function_name}: {exception.__class__.__name__}."
            response: Response = content.to_response()

        return response
