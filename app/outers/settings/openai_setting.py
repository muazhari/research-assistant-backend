from pydantic import BaseSettings


class OpenAiSetting(BaseSettings):
    OPEN_AI_API_KEY: str
    OPEN_AI_URL: str

    class Config:
        env_file = ".env"
