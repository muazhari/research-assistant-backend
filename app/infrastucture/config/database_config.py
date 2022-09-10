import os

from pydantic import BaseSettings


class DatabaseConfig(BaseSettings):
    DATABASE_DIALECT = os.getenv("DATABASE_DIALECT", "sqlite")
    DATABASE_USER = os.getenv("DATABASE_USER", "admin")
    DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", "password")
    DATABASE_HOST = os.getenv("DATABASE_HOST", "localhost")
    DATABASE_PORT = os.getenv("DATABASE_PORT", "5432")
    DATABASE_NAME = os.getenv("DATABASE_NAME", "local_db")

    if DATABASE_DIALECT == "sqlite":
        DATABASE_URL = "sqlite:///local_db.sqlite3"
    else:
        DATABASE_URL = f"{DATABASE_DIALECT}://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"


database_config = DatabaseConfig()
