from typing import Any

import asyncpg
import sqlalchemy
from sqlalchemy import exc
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

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

    async def get_session(self):
        session = AsyncSession(
            bind=self.engine
        )
        return session

    class MaxRetriesException(Exception):
        def __init__(self, *args):
            super().__init__(*args)

    async def retryable(self, func, max_retries: int = 10):
        retry_count = 0
        while retry_count < max_retries:
            session: AsyncSession = await self.get_session()
            try:
                await session.begin()
                result: Any = await func(session)
                await session.commit()
                break
            except Exception as exception:
                await session.rollback()
                if isinstance(exception, sqlalchemy.exc.DBAPIError):
                    if exception.orig.pgcode == asyncpg.exceptions.SerializationError.sqlstate:
                        retry_count += 1
                        continue
                raise exception

        if retry_count == max_retries:
            raise self.MaxRetriesException("OneDatastore.retryable: Retry count is equal to max retries.")

        return result
