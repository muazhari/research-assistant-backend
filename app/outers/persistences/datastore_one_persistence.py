from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.pool import NullPool
from sqlmodel.ext.asyncio.session import AsyncSession

from app.outers.settings.datastore_one_setting import DatastoreOneSetting


class DataStoreUtility:
    def __init__(self):
        self.datastore_one_setting = DatastoreOneSetting()
        self.engine = create_async_engine(
            url=self.datastore_one_setting.URL,
            poolclass=NullPool,
        )

    async def create_session(self) -> AsyncSession:
        async with AsyncSession(self.engine) as session:
            return session
