from redis import Redis as SyncRedis
from redis.asyncio import Redis as AsyncRedis

from apps.outers.settings.two_datastore_setting import TwoDatastoreSetting


class TwoDatastore:

    def __init__(
            self,
            two_datastore_setting: TwoDatastoreSetting
    ):
        self.two_datastore_setting: TwoDatastoreSetting = two_datastore_setting
        self.async_client: AsyncRedis = AsyncRedis.from_url(
            url=self.two_datastore_setting.URL
        )
        self.sync_client: SyncRedis = SyncRedis.from_url(
            url=self.two_datastore_setting.URL
        )
