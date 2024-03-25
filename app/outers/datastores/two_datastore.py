import redis
from redis.asyncio import Redis

from app.outers.settings.two_datastore_setting import TwoDatastoreSetting


class TwoDatastore:

    def __init__(
            self,
            two_datastore_setting: TwoDatastoreSetting
    ):
        self.two_datastore_setting: TwoDatastoreSetting = two_datastore_setting
        self.client: Redis = Redis.from_url(
            url=self.two_datastore_setting.URL
        )
        # loop = asyncio.get_event_loop()
        # self.client = loop.run_until_complete(self.client.initialize())
        # loop.close()
