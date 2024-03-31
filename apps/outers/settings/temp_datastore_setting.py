from pathlib import Path

from apps.outers.settings.base_setting import BaseSetting


class TempDatastoreSetting(BaseSetting):
    TEMP_DATASTORE_PATH: Path

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
