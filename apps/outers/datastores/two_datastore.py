from redis.asyncio import Redis

from apps.outers.settings.two_datastore_setting import TwoDatastoreSetting


class TwoDatastore:

    def __init__(
            self,
            two_datastore_setting: TwoDatastoreSetting
    ):
        self.two_datastore_setting: TwoDatastoreSetting = two_datastore_setting
        self.client: Redis = Redis.from_url(
            url=self.two_datastore_setting.URL
        )
