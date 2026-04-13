from enum import StrEnum
from typing import List, Literal

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

    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: str = ""
    REDIS_MAX_CONNECTIONS: int = 50
    REDIS_SOCKET_TIMEOUT: int = 5
    REDIS_SOCKET_CONNECT_TIMEOUT: int = 5
    REDIS_DECODE_RESPONSES: bool = True
    REDIS_HEALTH_CHECK_INTERVAL: int = 30

    # Redis Key Prefixes
    REDIS_TOKEN_REVOKE_PREFIX: str = "TOKEN_REVOKED"

    # Cookie
    COOKIE_SECURE: bool = Field(
        False, description="Set to False only in development (allows HTTP)"
    )
    COOKIE_SAMESITE: Literal["lax", "strict", "none"] = Field(
        "lax", description="SameSite poicy"
    )
    COOKIE_DOMAIN: str | None = Field(
        None, description="Cookie domain. None = current domain only"
    )
    COOKIE_ACCESS_TOKEN_KEY: str = Field(
        "ACCESS_TOKEN",
        description="Access token key",
    )
    COOKIE_REFRESH_TOKEN_KEY: str = Field(
        "REFRESH_TOKEN",
        description="Refresh token key",
    )

    # CORS
    CORS_ALLOW_ORIGINS: List[str] = ["http://localhost:3000"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: List[str] = ["*"]
    CORS_ALLOW_HEADERS: List[str] = ["*"]

    # Resend
    RESEND_API_KEY: str = "re_..."
    RESEND_FROM_EMAIL: str = "noreplay@yourdomain.com"
    FRONTEND_URL: str = "http://localhost:8000"

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
