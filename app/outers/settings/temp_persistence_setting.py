from pathlib import Path

from pydantic import BaseSettings


class TempPersistenceSetting(BaseSettings):
    PATH: Path = "app/outers/persistences/temps"
