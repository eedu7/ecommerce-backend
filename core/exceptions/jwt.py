from __future__ import annotations

from typing import Any, Dict

from core.exceptions.base import UnauthorizedException


class TokenExpiredException(UnauthorizedException):
    """
    Raised when a JWT token's 'exp' claim is in the past.

    HTTP Status: 401 Unauthorized
    """

    def __init__(
        self, message: str = "Token has expired", headers: Dict[str, str] | None = None
    ) -> None:
        super().__init__(message=message, error_code="TOKEN_EXPIRED", headers=headers)


class InvalidTokenException(UnauthorizedException):
    """
    Raised when a JWT fails signature verification, cannot be decoded,
    has an invalid issuer/audience, or is structurally malformed.

    HTTP Status: 401 Unauthorized
    """

    def __init__(
        self,
        message: str = "Invalid token",
        headers: Dict[str, str] | None = None,
        details: Dict[str, Any] | None = None,
    ) -> None:
        super().__init__(
            message=message,
            error_code="INVALID_TOKEN",
            headers=headers,
            details=details,
        )


class MissingTokenException(UnauthorizedException):
    """
    Raised when no token is present in the request.

    HTTP Status: 401 Unauthorized
    """

    def __init__(
        self,
        message: str = "Authentication token is missing",
        headers: Dict[str, str] | None = None,
    ) -> None:
        super().__init__(message=message, error_code="MISSING_TOKEN", headers=headers)


class TokenRevokedException(UnauthorizedException):
    """
    Raised when the token's 'jti' is found in the revocation store.

    HTTP Status: 401 Unauthorized
    """

    def __init__(
        self,
        message: str = "Token has been revoked",
        headers: Dict[str, str] | None = None,
    ) -> None:
        super().__init__(message=message, error_code="TOKEN_REVOKED", headers=headers)


class InvalidTokenTypeException(UnauthorizedException):
    """
    Raised when a token of the wrong type is presented (e.g. a refresh token used where an access token is required).

    HTTP Status: 401 Unauthorized
    """

    def __init__(
        self,
        expected: str,
        received: str,
        headers: Dict[str, str] | None = None,
    ) -> None:
        super().__init__(
            message=f"Invalid token type: Expected '{expected}, got '{received}')",
            error_code="INVALID_TOKEN_TYPE",
            headers=headers,
            details={"expected": expected, "got": received},
        )
