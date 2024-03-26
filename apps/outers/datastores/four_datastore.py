from typing import Any

from langchain_community.vectorstores.milvus import Milvus
from langchain_core.embeddings import Embeddings

from apps.outers.settings.four_datastore_setting import FourDatastoreSetting


class FourDatastore:

    def __init__(
            self,
            four_datastore_setting: FourDatastoreSetting
    ):
        self.four_datastore_setting: FourDatastoreSetting = four_datastore_setting

    def get_client(self, *args: Any, **kwargs: Any) -> Milvus:
        return Milvus(
            connection_args=self._get_connection_args(),
            *args,
            **kwargs
        )

    def _get_connection_args(self):
        return {
            "host": self.four_datastore_setting.DS_FOUR_HOST,
            "port": self.four_datastore_setting.DS_FOUR_PORT,
            "user": self.four_datastore_setting.DS_FOUR_USER,
            "password": self.four_datastore_setting.DS_FOUR_PASSWORD,
        }
