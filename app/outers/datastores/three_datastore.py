from miniopy_async import Minio

from app.outers.settings.three_datastore_setting import ThreeDatastoreSetting


class ThreeDatastore:

    def __init__(
            self,
            three_datastore_setting: ThreeDatastoreSetting
    ):
        self.three_datastore_setting: ThreeDatastoreSetting = three_datastore_setting
        self.client: Minio = Minio(
            endpoint=f"{self.three_datastore_setting.DS_THREE_HOST}:{self.three_datastore_setting.DS_THREE_PORT}",
            access_key=self.three_datastore_setting.DS_THREE_USER,
            secret_key=self.three_datastore_setting.DS_THREE_PASSWORD,
            secure=False
        )
