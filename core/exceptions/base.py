from typing import Any, Dict

from fastapi import HTTPException, status


class CustomException(HTTPException):
    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        error_code: str | None = None,
        headers: Dict[str, str] | None = None,
        details: Dict[str, Any] | None = None,
    ) -> None:
        detail: Dict[str, Any] = {"message": message}
        if error_code:
            detail["error_code"] = error_code
        if details:
            detail["details"] = details

        self.message = message
        self.error_code = error_code
        super().__init__(status_code=status_code, detail=detail, headers=headers)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}: {self.message}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(message={self.message!r}, status_code={self.status_code})"


class BadRequestException(CustomException):
    """
    Raised when the request data is invalid or malformed.
    HTTP Status: 400 Bad Request
    """

    def __init__(
        self,
        message: str = "Bad Request",
        error_code: str | None = None,
        headers: Dict[str, str] | None = None,
        details: Dict[str, Any] | None = None,
    ) -> None:
        super().__init__(
            message=message,
            status_code=status.HTTP_400_BAD_REQUEST,
            error_code=error_code,
            headers=headers,
            details=details,
        )


class UnauthorizedException(CustomException):
    """
    Raised when authentication is missing or invalid.
    HTTP Status: 401 Unauthorized
    """

    def __init__(
        self,
        message: str = "Unauthorized",
        error_code: str | None = None,
        headers: Dict[str, str] | None = None,
        details: Dict[str, Any] | None = None,
    ) -> None:
        # Add WWW-Authenticate header by default if not provided
        if headers is None:
            headers = {"WWW-Authenticate": "Bearer"}
        super().__init__(
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED,
            error_code=error_code,
            headers=headers,
            details=details,
        )


class ForbiddenException(CustomException):
    """
    Raised when the client lacks permission to access the resource.
    HTTP Status: 403 Forbidden
    """

    def __init__(
        self,
        message: str = "Forbidden",
        error_code: str | None = None,
        headers: Dict[str, str] | None = None,
        details: Dict[str, Any] | None = None,
    ) -> None:
        super().__init__(
            message=message,
            status_code=status.HTTP_403_FORBIDDEN,
            error_code=error_code,
            headers=headers,
            details=details,
        )


class NotFoundException(CustomException):
    """
    Raised when the requested resource does not exist.
    HTTP Status: 404 Not Found
    """

    def __init__(
        self,
        message: str = "Not Found",
        error_code: str | None = None,
        headers: Dict[str, str] | None = None,
        details: Dict[str, Any] | None = None,
    ) -> None:
        super().__init__(
            message=message,
            status_code=status.HTTP_404_NOT_FOUND,
            error_code=error_code,
            headers=headers,
            details=details,
        )


class UnprocessableEntityException(CustomException):
    """
    Raised when the request is syntactically valid but semantically incorrect.
    HTTP Status: 422 Unprocessable Entity
    """

    def __init__(
        self,
        message: str = "Unprocessable Entity",
        error_code: str | None = None,
        headers: Dict[str, str] | None = None,
        details: Dict[str, Any] | None = None,
    ) -> None:
        super().__init__(
            message=message,
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            error_code=error_code,
            headers=headers,
            details=details,
        )


class TooManyRequestsException(CustomException):
    """
    Raised when rate limit is exceeded.
    HTTP Status: 429 Too Many Requests
    """

    def __init__(
        self,
        message: str = "Too Many Requests",
        error_code: str | None = None,
        headers: Dict[str, str] | None = None,
        details: Dict[str, Any] | None = None,
        retry_after: int | None = None,  # Seconds until retry is allowed
    ) -> None:
        if retry_after is not None:
            if headers is None:
                headers = {}
            headers["Retry-After"] = str(retry_after)

        super().__init__(
            message=message,
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            error_code=error_code,
            headers=headers,
            details=details,
        )


class InternalServerException(CustomException):
    """
    Raised when an unexpected internal server error occurs.
    HTTP Status: 500 Internal Server Error
    """

    def __init__(
        self,
        message: str = "Internal Server Error",
        error_code: str | None = None,
        headers: Dict[str, str] | None = None,
        details: Dict[str, Any] | None = None,
    ) -> None:
        super().__init__(
            message=message,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_code=error_code,
            headers=headers,
            details=details,
        )


class NotImplementedException(CustomException):
    """
    Raised when the requested feature is not yet implemented
    HTTP Status: 501 Not Implemented
    """

    def __init__(
        self,
        message: str = "Not Implemented",
        error_code: str | None = None,
        headers: Dict[str, str] | None = None,
        details: Dict[str, Any] | None = None,
    ) -> None:
        super().__init__(
            message=message,
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            error_code=error_code,
            headers=headers,
            details=details,
        )


class DatabaseException(CustomException):
    """
    Raised when a database operation fails.
    HTTP Status: 500 Internal Server Error
    """

    def __init__(
        self,
        message: str = "Database Error",
        error_code: str | None = "DATABASE_ERROR",
        headers: dict[str, str] | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(
            message=message,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_code=error_code,
            headers=headers,
            details=details,
        )


class DuplicateValueException(CustomException):
    """
    Raised when a duplicate or unique constraint violation occurs.
    HTTP Status: 409 Conflict
    """

    def __init__(
        self,
        message: str = "Duplicate Value",
        error_code: str | None = "DUPLICATE_VALUE",
        headers: dict[str, str] | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(
            message=message,
            status_code=status.HTTP_409_CONFLICT,
            error_code=error_code,
            headers=headers,
            details=details,
        )


class PermissionDeniedException(ForbiddenException):
    """
    Raised when user lacks required permissions.
    HTTP Status: 403 Forbidden

    Use when: Role-based access denied, insufficient privileges
    """

    def __init__(
        self,
        message: str = "Permission Denied",
        error_code: str | None = "PERMISSION_DENIED",
        headers: dict[str, str] | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(
            message=message,
            error_code=error_code,
            headers=headers,
            details=details,
        )


class ResourceNotFoundException(NotFoundException):
    """
    Raised when a specific resource is not found.
    HTTP Status: 404 Not Found

    Use when: User not found, Product not found, etc.
    """

    def __init__(
        self,
        resource: str,
        resource_id: str | int,
        error_code: str | None = "RESOURCE_NOT_FOUND",
        headers: dict[str, str] | None = None,
    ) -> None:
        super().__init__(
            message=f"{resource} with id '{resource_id}' not found",
            error_code=error_code,
            headers=headers,
            details={"resource": resource, "resource_id": str(resource_id)},
        )


class RateLimitExceededException(TooManyRequestsException):
    """
    Raised when API rate limit is exceeded.
    HTTP Status: 429 Too Many Requests

    Use when: Request quota exceeded, throttling applied
    """

    def __init__(
        self,
        message: str = "Rate Limit Exceeded",
        error_code: str | None = "RATE_LIMIT_EXCEEDED",
        retry_after: int = 60,
        limit: int | None = None,
        headers: dict[str, str] | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        if details is None:
            details = {}

        details["retry_after"] = retry_after
        if limit is not None:
            details["limit"] = limit

        super().__init__(
            message=message,
            error_code=error_code,
            headers=headers,
            details=details,
            retry_after=retry_after,
        )
