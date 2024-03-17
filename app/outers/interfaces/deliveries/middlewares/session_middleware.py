from typing import Any

from sqlmodel.ext.asyncio.session import AsyncSession
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp

from app.inners.models.dtos.contracts.content import Content
from app.inners.models.dtos.contracts.result import Result
from app.outers.datastores.one_datastore import OneDatastore


class SessionMiddleware(BaseHTTPMiddleware):
    def __init__(
            self,
            app: ASGIApp,
            one_datastore: OneDatastore
    ):
        super().__init__(app)
        self.one_datastore = one_datastore

    class HandlerException(Exception):
        def __init__(self, result: Result[Any], *args: object) -> None:
            super().__init__(*args)
            self.result = result

    async def dispatch(
            self,
            request: Request,
            call_next: RequestResponseEndpoint
    ) -> Response:
        try:
            async def handler(session: AsyncSession):
                request.state.session = session
                try:
                    handler_response: Response = await call_next(request)
                except SessionMiddleware.HandlerException as handler_exception:
                    handler_response: Response = Response(
                        status_code=handler_exception.result.status_code,
                        content=Content(
                            message=f"SessionMiddleware.dispatch: Failed, {handler_exception.result.message}",
                            data=None
                        ).json()
                    )
                return handler_response

            response: Response = await self.one_datastore.retryable(handler)
        except Exception as exception:
            # response: Response = Response(
            #     status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            #     content=Content(
            #         message=f"SessionMiddleware.dispatch: Failed, {exception}",
            #         data=None
            #     ).json()
            # )
            raise exception

        return response
