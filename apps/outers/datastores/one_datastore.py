import traceback
from typing import Any

import asyncpg
import sqlalchemy
from sqlalchemy import exc
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from apps.inners.exceptions import datastore_exception
from apps.outers.settings.one_datastore_setting import OneDatastoreSetting


class OneDatastore:

    def __init__(
            self,
            one_datastore_setting: OneDatastoreSetting
    ):
        self.one_datastore_setting: OneDatastoreSetting = one_datastore_setting
        self.engine: AsyncEngine = create_async_engine(
            url=self.one_datastore_setting.URL,
            isolation_level="SERIALIZABLE"
        )

    def get_session(self):
        session = AsyncSession(
            bind=self.engine
        )
        return session

    async def retryable(self, handler, max_retries: int = 10) -> Any:
        retry_count: int = 0
        while retry_count <= max_retries:
            session: AsyncSession = self.get_session()
            try:
                await session.begin()
                result: Any = await handler(session)
                await session.commit()
                await session.close()
                return result
            except sqlalchemy.exc.DBAPIError as exception:
                await session.rollback()
                await session.close()
                if exception.orig.pgcode == asyncpg.exceptions.SerializationError.sqlstate:
                    retry_count += 1
                    continue
            except Exception:
                await session.rollback()
                await session.close()
                traceback.print_exc()
                raise datastore_exception.HandlerError()

        raise datastore_exception.MaxRetriesExceeded()
