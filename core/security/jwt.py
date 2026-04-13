from datetime import datetime, timedelta, timezone
from typing import Any, Dict
from uuid import uuid4

import jwt
from jwt import (
    DecodeError,
    ExpiredSignatureError,
    ImmatureSignatureError,
    InvalidAlgorithmError,
    InvalidAudienceError,
    InvalidIssuerError,
    InvalidSignatureError,
    MissingRequiredClaimError,
)

from app.schemas.extras.token import Token, TokenPayload, TokenType
from core.config import config
from core.dependencies.stores import RevokeTokenStoreDep
from core.exceptions import InternalServerException
from core.exceptions.jwt import (
    InvalidTokenException,
    InvalidTokenTypeException,
    MissingTokenException,
    TokenExpiredException,
)
from core.stores import RevokeTokenStore


def _build_payload(raw: Dict[str, Any]) -> TokenPayload:
    known_keys = {"sub", "type", "jti", "iat", "exp", "nbf", "iss", "aud"}

    try:
        return TokenPayload(
            sub=raw["sub"],
            type=raw["type"],
            jti=raw["jti"],
            iat=datetime.fromtimestamp(raw["iat"], tz=timezone.utc),
            exp=datetime.fromtimestamp(raw["exp"], tz=timezone.utc),
            nbf=(
                datetime.fromtimestamp(raw["nbf"], tz=timezone.utc)
                if "nbf" in raw
                else None
            ),
            iss=raw.get("iss"),
            aud=raw.get("aud"),
            extra={key: value for key, value in raw.items() if key not in known_keys},
        )
    except (KeyError, ValueError) as exc:
        raise InvalidTokenException(
            message=f"Token payload is malformed: {exc}"
        ) from exc


class JWTService:
    def __init__(self, store: RevokeTokenStore) -> None:
        self.store = store
        self.jwt_access_token_expire_minute: int = (
            config.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
        )
        self.jwt_refresh_token_expire_days: int = config.JWT_REFRESH_TOKEN_EXPIRE_DAYS
        self.jwt_secret_key: str = config.JWT_SECRET_KEY
        self.jwt_algorithm: str = config.JWT_ALGORITHM
        self.jwt_issuer: str | None = config.JWT_ISSUER
        self.jwt_audience: str | None = config.JWT_AUDIENCE
        self.jwt_leeway_seconds: int = config.JWT_LEEWAY_SECONDS

    def build_token_pair(
        self,
        subject: str,
        extra_claims: Dict[str, Any] | None = None,
    ) -> Token:
        access_ttl = timedelta(minutes=self.jwt_access_token_expire_minute)
        refresh_ttl = timedelta(days=self.jwt_refresh_token_expire_days)

        claims = extra_claims or {}

        access_token = self._build_token(
            subject,
            "access",
            ttl=access_ttl,
            extra_claims=claims,
        )
        refresh_token = self._build_token(
            subject,
            "refresh",
            ttl=refresh_ttl,
            extra_claims=claims,
        )

        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=int(access_ttl.total_seconds()),
        )

    def decode_token(
        self,
        token: str | None,
        *,
        expected_token: TokenType | None = None,
        verify_exp: bool = True,
    ) -> TokenPayload:
        if not token or not token.strip():
            raise MissingTokenException()

        raw_payload = self._decode_jwt(token=token, verify_exp=verify_exp)
        payload = _build_payload(raw_payload)

        if expected_token is not None and payload.type != expected_token:
            raise InvalidTokenTypeException(
                expected=expected_token, received=payload.type
            )

        return payload

    def refresh_access_token(
        self, refresh_token: str, extra_claims: Dict[str, Any] | None = None
    ) -> Token:
        payload = self.decode_token(refresh_token, expected_token="refresh")

        return self.build_token_pair(
            subject=payload.sub, extra_claims={**payload.extra, **(extra_claims or {})}
        )

    async def revoke_tokens(
        self, access_token: str | None = None, refresh_token: str | None = None
    ) -> None:
        if access_token:
            access_payload = self.decode_expired_token(access_token)
            await self._revoke_token(
                access_payload.jti, self.jwt_access_token_expire_minute * 60
            )

        if refresh_token:
            refresh_payload = self.decode_expired_token(refresh_token)
            await self._revoke_token(
                refresh_payload.jti, self.jwt_refresh_token_expire_days * 24 * 60 * 60
            )

    async def _revoke_token(self, jti: str, ttl: int | None = None) -> None:
        if ttl is None:
            ttl = self.jwt_access_token_expire_minute * 60
        await self.store.revoke(jti, ttl=ttl)

    async def revoke_token_by_raw(self, token: str) -> None:
        payload = self.decode_token(token, verify_exp=False)
        await self._revoke_token(payload.jti)

    async def is_token_revoked(self, jti: str) -> bool:
        return await self.store.is_revoked(jti)

    def decode_expired_token(self, token: str) -> TokenPayload:
        return self.decode_token(token, verify_exp=False)

    def _build_token(
        self,
        subject: str,
        token_type: TokenType,
        ttl: timedelta,
        extra_claims: Dict[str, Any],
    ) -> str:
        now = datetime.now(tz=timezone.utc)

        payload: Dict[str, Any] = {
            "sub": subject,
            "type": token_type,
            "jti": str(uuid4()),
            "iat": now,
            "nbf": now,
            "exp": now + ttl,
            **extra_claims,
        }

        if self.jwt_issuer:
            payload["iss"] = self.jwt_issuer
        if self.jwt_audience:
            payload["aud"] = self.jwt_audience

        try:
            return jwt.encode(
                payload, key=self.jwt_secret_key, algorithm=self.jwt_algorithm
            )
        except Exception as exc:
            raise InternalServerException(
                message="Token creation failed", details={"reason": str(exc)}
            ) from exc

    def _decode_jwt(self, token: str, *, verify_exp: bool) -> Dict[str, Any]:
        options: Dict[str, Any] = {
            "verify_exp": verify_exp,
            "verify_nbf": True,
            "verify_iss": bool(self.jwt_issuer),
            "verify_aud": bool(self.jwt_audience),
            "require": ["sub", "jti", "iat", "exp", "type"],
        }

        decode_kwargs: Dict[str, Any] = {
            "algorithms": [self.jwt_algorithm],
            "options": options,
            "leeway": timedelta(seconds=self.jwt_leeway_seconds),
        }
        if self.jwt_issuer:
            decode_kwargs["issuer"] = self.jwt_issuer
        if self.jwt_audience:
            decode_kwargs["audience"] = self.jwt_audience

        try:
            return jwt.decode(token, key=self.jwt_secret_key, **decode_kwargs)
        except ExpiredSignatureError as exc:
            raise TokenExpiredException() from exc
        except InvalidSignatureError as exc:
            raise InvalidTokenException(
                message="Token signature verification failed"
            ) from exc
        except (InvalidIssuerError, InvalidAudienceError) as exc:
            raise InvalidTokenException(message=str(exc)) from exc
        except MissingRequiredClaimError as exc:
            raise InvalidTokenException(
                message=f"Token is missing required claim: {exc.claim}"
            ) from exc
        except InvalidAlgorithmError as exc:
            raise InvalidTokenException(
                message=f"Token uses an unsupported algorithm: {exc}"
            ) from exc
        except DecodeError as exc:
            raise InvalidTokenException(
                message="Token could not be decoded - it may be malformed"
            ) from exc
        except ImmatureSignatureError as exc:
            raise InvalidTokenException(
                message="Token is not yet valid (nbf claim)"
            ) from exc
        except Exception as exc:
            raise InternalServerException(
                message="Token validation encountered an unexpected error",
                details={"reason": str(exc)},
            ) from exc


def get_jwt_service(store: RevokeTokenStoreDep) -> JWTService:
    return JWTService(store)
