import os
from typing import Any

from pydantic import BaseSettings


class DatabaseSettings(BaseSettings):
    DATABASE_DIALECT: str = None
    DATABASE_URL: str = None
    DATABASE_HOST: str = None
    DATABASE_PORT: str = None
    DATABASE_USER: str = None
    DATABASE_PASSWORD: str = None
    DATABASE_NAME: str = None

    class Config:
        env_file = ".env"

    def __init__(self, **values: Any):
        super().__init__(**values)
        if self.DATABASE_DIALECT == "sqlite":
            self.DATABASE_URL = f"{self.DATABASE_DIALECT}:///{self.DATABASE_NAME}.sqlite3"
        elif self.DATABASE_DIALECT == "postgresql":
            self.DATABASE_URL = f"{self.DATABASE_DIALECT}://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"
        else:
            raise ValueError(f"Database dialect {self.DATABASE_DIALECT} is not supported.")


database_settings = DatabaseSettings()
