import httpx


class BaseClient:
    def __init__(self):
        self.base_url = None

    async def get_client(self):
        return httpx.Client(base_url=self.base_url)
