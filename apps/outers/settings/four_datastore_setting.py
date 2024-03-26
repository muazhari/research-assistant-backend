from typing import Any

from dotenv import find_dotenv
from pydantic import BaseSettings


class FourDatastoreSetting(BaseSettings):
    DS_FOUR_HOST: str
    DS_FOUR_PORT: str
    DS_FOUR_USER: str
    DS_FOUR_PASSWORD: str

    class Config:
        env_file = find_dotenv(".env")

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
