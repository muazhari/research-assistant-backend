from dotenv import find_dotenv
from pydantic_settings import BaseSettings


class BaseSetting(BaseSettings):
    class Config:
        env_file = find_dotenv(".env")
        extra = "ignore"
