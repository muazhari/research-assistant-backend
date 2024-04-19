from typing import Optional, Any

from apps.outers.settings.base_setting import BaseSetting


class TwoDatastoreSetting(BaseSetting):
    DS_TWO_HOST: str
    DS_TWO_PORT: str
    DS_TWO_USER: str
    DS_TWO_PASSWORD: str
    URL: Optional[str] = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.URL = f"redis://{self.DS_TWO_USER}:{self.DS_TWO_PASSWORD}@{self.DS_TWO_HOST}:{self.DS_TWO_PORT}"
