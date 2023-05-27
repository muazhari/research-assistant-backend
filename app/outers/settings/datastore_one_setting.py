from typing import Optional

from pydantic import BaseSettings


class DatastoreOneSetting(BaseSettings):
    DS_1_DIALECT: str
    DS_1_HOST: str
    DS_1_PORT: str
    DS_1_USER: str
    DS_1_PASSWORD: str
    DS_1_DATABASE: str
    URL: Optional[str] = None

    class Config:
        env_file = ".env"

    def __init__(self, **kwargs: any):
        super().__init__(**kwargs)
        self.URL = f"{self.DS_1_DIALECT}://{self.DS_1_USER}:{self.DS_1_PASSWORD}@{self.DS_1_HOST}:{self.DS_1_PORT}/{self.DS_1_DATABASE}"
