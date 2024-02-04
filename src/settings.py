import os
from enum import Enum

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings


class Environment(str, Enum):
    DEVELOPMENT = "development"
    TEST = "test"
    PRODUCTION = "production"


class Settings(BaseSettings):
    BASE_DIR: str = os.path.dirname(os.path.abspath(__file__))

    ENV: Environment = Environment.DEVELOPMENT

    COUNTRY_API_URL: str = "https://restcountries.com/v3.1/all"

    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    @staticmethod
    def _get_db_name(env, initial_value):
        if env == Environment.TEST:
            return initial_value + "_test"
        return initial_value

    @property
    def DB_CONNECTION(self) -> str:
        return str(
            PostgresDsn.build(
                scheme="postgresql",
                host=self.DB_HOST,
                port=self.DB_PORT,
                path=f"{Settings._get_db_name(self.ENV, self.DB_NAME)}",
                username=self.DB_USER,
                password=self.DB_PASSWORD,
            )
        )


settings = Settings()
