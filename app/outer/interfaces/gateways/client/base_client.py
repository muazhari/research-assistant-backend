import json

import aiohttp
from fastapi.encoders import jsonable_encoder


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        return jsonable_encoder(obj)


class BaseClient:
    def __init__(self):
        self.base_url = None

    async def get_client_session(self):
        return aiohttp.ClientSession(base_url=self.base_url,
                                     json_serialize=lambda object_to_serialize: json.dumps(
                                         object_to_serialize,
                                         indent=4,
                                         sort_keys=True,
                                         cls=CustomEncoder)
                                     )
