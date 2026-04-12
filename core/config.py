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

    # JWT
    JWT_SECRET_KEY: str = Field(
        "YOUR_JWT_SECRET_KEY",
        description="HMAC secret key used to sign and verify tokens. Generate with: openssl rand -hex 32",
    )
    JWT_ALGORITHM: str = Field(
        "HS256",
        description="JWT algorithm Identifier. Symmetric: HS256/HS384/HS512. Asymmetric: RS256/RS384/RS512 (required key pair)",
    )
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        15, gt=0, description="Access token lifetime in minutes"
    )
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = Field(
        7, gt=0, description="Refresh token lifetime in days"
    )
    JWT_ISSUER: str | None = Field(
        None,
        description="Value for the 'iss' claim. When set, all issued tokens include it and incoming tokens are validated against it.",
    )
    JWT_AUDIENCE: str | None = Field(
        None,
        description="Value for the 'aud' claim. When set, all issued tokens include it and incoming tokens are validated against it.",
    )
    JWT_LEEWAY_SECONDS: int = Field(
        0,
        ge=0,
        description="Clock-skew tolerance applied when validating 'exp' and 'nbf'. Keep at 0 in production; raise only for cross-service clock drift",
    )

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
