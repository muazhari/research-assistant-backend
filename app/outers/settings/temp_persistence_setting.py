from pathlib import Path

from pydantic import BaseSettings


class TempPersistenceSetting(BaseSettings):
    TEMP_PERSISTENCE_PATH: Path
