from pathlib import Path

from apps.outers.settings.base_setting import BaseSetting


class TempDatastoreSetting(BaseSetting):
    TEMP_DATASTORE_PATH: Path
