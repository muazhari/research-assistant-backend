from typing import Optional, Any

from dotenv import find_dotenv
from pydantic import BaseSettings


class ThreeDatastoreSetting(BaseSettings):
    DS_THREE_HOST: str
    DS_THREE_PORT: str
    DS_THREE_USER: str
    DS_THREE_PASSWORD: str

    class Config:
        env_file = find_dotenv(".env")

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
