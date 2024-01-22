from pathlib import Path

from pydantic import BaseSettings


class TempDatastoreSetting(BaseSettings):
    TEMP_DATASTORE_PATH: Path

    class Config:
        env_file = ".env"
