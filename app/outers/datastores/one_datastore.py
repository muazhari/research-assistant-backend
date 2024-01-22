from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.orm import sessionmaker, Session
from sqlmodel import create_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from app.outers.settings.one_datastore_setting import OneDatastoreSetting


class OneDatastore:
    def __init__(
            self,
            one_datastore_setting: OneDatastoreSetting
    ):
        self.one_datastore_setting: OneDatastoreSetting = one_datastore_setting
        self.engine: AsyncEngine = AsyncEngine(create_engine(
            url=self.one_datastore_setting.URL,
            echo=True,
            future=True
        ))

    async def create_session(self) -> Session:
        async_session = sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )
        return async_session()
