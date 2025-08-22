from typing import Literal

from pydantic.v1 import validator
from pydantic_settings import BaseSettings
from pydantic import Field, MySQLDsn


class EnvConfig(BaseSettings):
    """仅用于读取当前环境"""
    CURRENT_ENV: Literal["local", "development", "staging","dev", "production"] = "staging"
    # CURRENT_ENV: "local" | "development" | "staging" | "production" | str = "development"


    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

class DatabaseSettings(BaseSettings):
    MYSQL_HOST: str
    MYSQL_PORT: int = 3306
    MYSQL_USER: str
    MYSQL_PASSWORD: str = Field(..., exclude=True)
    MYSQL_DATABASE: str
    POOL_SIZE: int

    @property
    def DATABASE_URL(self) -> MySQLDsn:
        return f"mysql+pymysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DATABASE}"

    class Config:
        env_file = ".env."+EnvConfig().CURRENT_ENV
        extra = "ignore"


settings = DatabaseSettings()