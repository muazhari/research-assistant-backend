import json

import aiohttp

from app.infrastucture.config.client_config import client_config


class BaseClient:

    async def get_client_session(self):
        return aiohttp.ClientSession(base_url=client_config.CLIENT_TRANSACTION_URL,
                                     json_serialize=lambda object_to_serialize: json.dumps(
                                         object_to_serialize,
                                         indent=4,
                                         sort_keys=True,
                                         default=str)
                                     )
