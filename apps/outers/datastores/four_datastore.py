import uuid
from typing import Any, Optional, Dict, Union

from langchain_community.vectorstores.milvus import Milvus
from pymilvus import connections

from apps.outers.settings.four_datastore_setting import FourDatastoreSetting


class FourDatastore:

    def __init__(
            self,
            four_datastore_setting: FourDatastoreSetting
    ):
        self.four_datastore_setting: FourDatastoreSetting = four_datastore_setting
        self.alias = self.get_connection_alias(self.get_connection_args())

    def get_connection_alias(self, connection_args: Dict[str, Any]) -> str:
        host: Optional[str] = connection_args.get("host", None)
        port: Optional[Union[str, int]] = connection_args.get("port", None)
        address: Optional[str] = connection_args.get("address", None)
        uri: Optional[str] = connection_args.get("uri", None)
        user = connection_args.get("user", None)

        if host is not None and port is not None:
            given_address = str(host) + ":" + str(port)
        elif uri is not None:
            if uri.startswith("https://"):
                given_address = uri.split("https://")[1]
            elif uri.startswith("http://"):
                given_address = uri.split("http://")[1]
            else:
                raise ValueError("Invalid Milvus URI: %s.", uri)
        elif address is not None:
            given_address = address
        else:
            given_address = None

        if user is not None:
            tmp_user = user
        else:
            tmp_user = ""

        if given_address is not None:
            for con in connections.list_connections():
                addr = connections.get_connection_addr(con[0])
                if (
                        con[1]
                        and ("address" in addr)
                        and (addr["address"] == given_address)
                        and ("user" in addr)
                        and (addr["user"] == tmp_user)
                ):
                    return con[0]

        alias = uuid.uuid4().hex
        connections.connect(alias=alias, **connection_args)
        return alias

    def get_vector_store(self, *args: Any, **kwargs: Any) -> Milvus:
        return Milvus(
            connection_args=self.get_connection_args(),
            *args,
            **kwargs
        )

    def get_connection_args(self):
        return {
            "host": self.four_datastore_setting.DS_FOUR_HOST,
            "port": self.four_datastore_setting.DS_FOUR_PORT,
            "user": self.four_datastore_setting.DS_FOUR_USER,
            "password": self.four_datastore_setting.DS_FOUR_PASSWORD,
        }
