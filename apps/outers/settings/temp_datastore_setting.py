from pathlib import Path

from dotenv import find_dotenv
from pydantic import BaseSettings


class TempDatastoreSetting(BaseSettings):
    TEMP_DATASTORE_PATH: Path

    class Config:
        env_file = find_dotenv(".env")
