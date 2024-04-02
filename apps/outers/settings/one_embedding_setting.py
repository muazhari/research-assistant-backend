from typing import Optional, Any

from apps.outers.settings.base_setting import BaseSetting


class OneEmbeddingSetting(BaseSetting):
    EMBEDDING_ONE_HOST: str
    EMBEDDING_ONE_PORT: int
    URL: Optional[str] = None

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.URL = f"http://{self.EMBEDDING_ONE_HOST}:{self.EMBEDDING_ONE_PORT}"
