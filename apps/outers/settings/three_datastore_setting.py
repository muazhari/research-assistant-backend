from typing import Any

from apps.outers.settings.base_setting import BaseSetting


class ThreeDatastoreSetting(BaseSetting):
    DS_THREE_HOST: str
    DS_THREE_PORT: str
    DS_THREE_USER: str
    DS_THREE_PASSWORD: str

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
