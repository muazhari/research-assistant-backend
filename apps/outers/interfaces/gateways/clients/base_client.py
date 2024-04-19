import httpx


class BaseClient:
    def __init__(
            self,
            base_url: str = None,
    ):
        self.base_url = base_url

    async def get_client(self):
        return httpx.Client(base_url=self.base_url)
