from typing import Optional, Any

from dotenv import find_dotenv
from pydantic import BaseSettings


class OneDatastoreSetting(BaseSettings):
    DS_1_HOST: str
    DS_1_PORT: str
    DS_1_USER: str
    DS_1_PASSWORD: str
    DS_1_DATABASE: str
    URL: Optional[str] = None

    class Config:
        env_file = find_dotenv(".env")

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        if self.DS_1_PASSWORD == "":
            self.URL = f"cockroachdb+asyncpg://{self.DS_1_USER}@{self.DS_1_HOST}:{self.DS_1_PORT}/{self.DS_1_DATABASE}"
        else:
            self.URL = f"cockroachdb+asyncpg://{self.DS_1_USER}:{self.DS_1_PASSWORD}@{self.DS_1_HOST}:{self.DS_1_PORT}/{self.DS_1_DATABASE}"
