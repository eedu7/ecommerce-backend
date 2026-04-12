from enum import StrEnum

from pydantic import Field, PostgresDsn, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(StrEnum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"
    TESTING = "testing"


class Config(BaseSettings):
    # Project Environment
    ENVIRONMENT: Environment = Environment.DEVELOPMENT

    # Database
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "my_db"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "password@123"
    DB_POOL_SIZE: int = 5
    DB_POOL_RECYCLE: int = 3600
    DB_POOL_PRE_PING: bool = True
    DB_MAX_OVERFLOW: int = 10

    # Password Hashing
    PASSWORD_TIME_COST: int = Field(2, description="Number of iterations")
    PASSWORD_MEMORY_COST: int = Field(65536, description="64 MiB in KiB")
    PASSWORD_PARALLELISM: int = Field(4, description="Number of threads")
    PASSWORD_HASH_LENGTH: int = Field(32, description="Hash length in bytes")
    PASSWORD_SALT_LENGTH: int = Field(16, description="Salt length in bytes")

    @computed_field
    @property
    def DATABASE_URL(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


config = Config()
