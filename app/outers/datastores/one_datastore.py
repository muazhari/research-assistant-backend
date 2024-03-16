from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from app.outers.settings.one_datastore_setting import OneDatastoreSetting


class OneDatastore:
    def __init__(
            self,
            one_datastore_setting: OneDatastoreSetting
    ):
        self.one_datastore_setting: OneDatastoreSetting = one_datastore_setting
        self.engine: AsyncEngine = create_async_engine(
            url=self.one_datastore_setting.URL
        )

    async def get_session(self):
        session = AsyncSession(
            bind=self.engine
        )
        return session
