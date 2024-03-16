import asyncpg
import sqlalchemy
from dependency_injector.wiring import inject
from sqlalchemy import exc
from starlette import status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from starlette.types import ASGIApp

from app.inners.models.dtos.contracts.content import Content
from app.outers.datastores.one_datastore import OneDatastore


class SessionMiddleware(BaseHTTPMiddleware):

    @inject
    def __init__(
            self,
            app: ASGIApp,
            one_datastore: OneDatastore
    ):
        super().__init__(app)
        self.one_datastore = one_datastore

    async def dispatch(self, request, call_next):
        max_retries = 3
        retry_count = 0
        while retry_count < max_retries:
            session = await self.one_datastore.get_session()
            try:
                await session.begin()
                request.state.session = session
                response: Response = await call_next(request)
                await session.commit()
            except sqlalchemy.exc.DBAPIError as exception:
                if exception.orig.pgcode == asyncpg.exceptions.SerializationError.sqlstate:
                    retry_count += 1
                    continue
                response: Response = Response(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    content=Content(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        message=f"SessionMiddleware.dispatch: database error {exception}",
                        data=None
                    )
                )
            except Exception as exception:
                await session.rollback()
                response: Response = Response(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    content=Content(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        message=f"SessionMiddleware.dispatch: transaction error {exception}",
                        data=None
                    )
                )

        if retry_count == max_retries:
            response: Response = Response(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=Content(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    message="SessionMiddleware.dispatch: Retry count is equal to max retries.",
                    data=None
                )
            )

        return response
