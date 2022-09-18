import json
from uuid import UUID

import aiohttp

from app.infrastucture.config.client_config import client_config

from fastapi.encoders import jsonable_encoder

from app.infrastucture.utility.java_bytes import java_encode


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, list) and all(isinstance(item, int) for item in obj):
            return java_encode(obj)
        else:
            return jsonable_encoder(obj)


class BaseClient:

    async def get_client_session(self):
        return aiohttp.ClientSession(base_url=client_config.CLIENT_TRANSACTION_URL,
                                     json_serialize=lambda object_to_serialize: json.dumps(
                                         object_to_serialize,
                                         indent=4,
                                         sort_keys=True,
                                         cls=CustomEncoder)
                                     )
