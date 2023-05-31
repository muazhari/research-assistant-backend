from pydantic import BaseSettings


class OpenAISetting(BaseSettings):
    OPEN_AI_API_KEY: str

    class Config:
        env_file = ".env"
