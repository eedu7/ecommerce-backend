import re

from pydantic import BaseModel, EmailStr, Field, field_validator

from app.models.user import DBUserRole


class AuthIn(BaseModel):
    username: str = Field(
        ...,
        min_length=3,
        max_length=32,
        description="Unique username",
        examples=["john_doe"],
    )
    email: EmailStr = Field(
        ..., description="Email address", examples=["john_doe@example.com"]
    )
    password: str = Field(
        ..., min_length=8, description="Password", examples=["Password@123"]
    )
    role: DBUserRole = Field(DBUserRole.CUSTOMER, description="User role")

    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str) -> str:
        if not re.match(r"^[a-zA-Z0-9._-]+$", v):
            raise ValueError(
                "Username can only contain letters, numbers, underscore (_), and hyphens (-)"
            )
        return v

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"\d", v):
            raise ValueError("Password must contain at least one digit")
        if not re.search(r"[!@#$%^&*(),.?\"':{}|<>]", v):
            raise ValueError("Password must contain at least one special character")
        return v


class AuthLogin(BaseModel):
    username_or_email: str = Field(
        ...,
        min_length=3,
        max_length=256,
        examples=["john_doe", "john_doe@example.com"],
    )
    password: str = Field(
        ..., min_length=8, description="Password", examples=["Password@123"]
    )

    @field_validator("username_or_email")
    @classmethod
    def validate_username_or_email(cls, v: str) -> str:
        v = v.strip()
        try:
            EmailStr(v)
            return v
        except Exception:
            pass

        if not re.match(r"^[a-zA-Z0-9._-]+$", v):
            "Username can only contain letters, numbers, underscore (_), and hyphens (-)"

        return v


class AuthLogout(BaseModel):
    access_token: str | None = None
    refresh_token: str | None = None
