from typing import Optional, Any

from dotenv import find_dotenv
from pydantic import BaseSettings


class TwoDatastoreSetting(BaseSettings):
    DS_TWO_HOST: str
    DS_TWO_PORT: str
    DS_TWO_USER: str
    DS_TWO_PASSWORD: str
    URL: Optional[str] = None

    class Config:
        env_file = find_dotenv(".env")

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.URL = f"redis://{self.DS_TWO_USER}:{self.DS_TWO_PASSWORD}@{self.DS_TWO_HOST}:{self.DS_TWO_PORT}"
