from typing import List

from minio import Minio

from apps.outers.settings.three_datastore_setting import ThreeDatastoreSetting


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
            secure=False,
        )
        self.bucket_names: List[str] = [
            "research-assistant-backend.file-documents"
        ]
        self.prepare_buckets(self.bucket_names)

    def prepare_buckets(self, bucket_names: List[str]):
        for bucket_name in bucket_names:
            if not self.client.bucket_exists(bucket_name):
                self.client.make_bucket(bucket_name)
