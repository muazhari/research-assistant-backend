from typing import Any

from apps.outers.settings.base_setting import BaseSetting


class FourDatastoreSetting(BaseSetting):
    DS_FOUR_HOST: str
    DS_FOUR_PORT: str
    DS_FOUR_USER: str
    DS_FOUR_PASSWORD: str

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
