from typing import Optional, Any

from dotenv import find_dotenv
from pydantic import BaseSettings


class OneDatastoreSetting(BaseSettings):
    DS_ONE_HOST: str
    DS_ONE_PORT: str
    DS_ONE_USER: str
    DS_ONE_PASSWORD: str
    DS_ONE_DATABASE: str
    URL: Optional[str] = None

    class Config:
        env_file = find_dotenv(".env")

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        if self.DS_ONE_PASSWORD == "":
            self.URL = f"cockroachdb+asyncpg://{self.DS_ONE_USER}@{self.DS_ONE_HOST}:{self.DS_ONE_PORT}/{self.DS_ONE_DATABASE}"
        else:
            self.URL = f"cockroachdb+asyncpg://{self.DS_ONE_USER}:{self.DS_ONE_PASSWORD}@{self.DS_ONE_HOST}:{self.DS_ONE_PORT}/{self.DS_ONE_DATABASE}"
