from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerificationError, VerifyMismatchError

from core.config import config


class PasswordService:
    def __init__(self) -> None:
        self._hasher = PasswordHasher(
            time_cost=config.PASSWORD_TIME_COST,
            memory_cost=config.PASSWORD_MEMORY_COST,
            parallelism=config.PASSWORD_PARALLELISM,
            hash_len=config.PASSWORD_HASH_LENGTH,
            salt_len=config.PASSWORD_SALT_LENGTH,
        )

    def hash_password(self, password: str) -> str:
        return self._hasher.hash(password)

    def verify_password(self, hashed_password: str, plain_password: str):
        try:
            self._hasher.verify(hashed_password, plain_password)
            return True
        except VerifyMismatchError:
            return False
        except (VerificationError, InvalidHashError) as exc:
            raise ValueError(f"Invalid password hash format: {str(exc)}")
