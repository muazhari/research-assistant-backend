from pydantic import BaseSettings


class DatastoreTwoSetting(BaseSettings):
    DS_2_HOST: str
    DS_2_USERNAME: str
    DS_2_PASSWORD: str
    DS_2_PORT_1: str
    DS_2_PORT_2: str
    DS_2_MANAGEMENT_PORT: str

    class Config:
        env_file = ".env"
