from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.orm import sessionmaker, Session
from sqlmodel import create_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from app.outers.settings.datastore_one_setting import DatastoreOneSetting


class DatastoreOnePersistence:
    def __init__(
            self,
            datastore_one_setting: DatastoreOneSetting
    ):
        self.datastore_one_setting: DatastoreOneSetting = datastore_one_setting
        self.engine: AsyncEngine = AsyncEngine(create_engine(
            url=self.datastore_one_setting.URL,
            echo=True,
            future=True
        ))

    async def create_session(self) -> Session:
        async_session = sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )
        return async_session()
