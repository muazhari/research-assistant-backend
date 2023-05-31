from pathlib import Path

from pydantic import BaseSettings


class TempPersistenceSetting(BaseSettings):
    TEMP_PATH: Path = "app/outers/persistences/temps"
