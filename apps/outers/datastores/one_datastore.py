from typing import Any

import asyncpg
import sqlalchemy
from sqlalchemy import exc
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from apps.outers.exceptions import datastore_exception
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

    async def retryable(self, func, max_retries: int = 10):
        retry_count = 0
        while retry_count < max_retries:
            session: AsyncSession = await self.get_session()
            try:
                await session.begin()
                result: Any = await func(session)
                await session.commit()
                break
            except sqlalchemy.exc.DBAPIError as exception:
                await session.rollback()
                if exception.orig.pgcode == asyncpg.exceptions.SerializationError.sqlstate:
                    retry_count += 1
                    continue
            except Exception as exception:
                await session.rollback()
                raise exception
            finally:
                await session.close()

        if retry_count == max_retries:
            raise datastore_exception.MaxRetriesExceeded()

        return result
