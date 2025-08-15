from pydantic_settings import BaseSettings
from pydantic import Field, MySQLDsn


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
        env_file = ".env.dev"
        extra = "ignore"


settings = DatabaseSettings()