from app.models import DBUser
from app.repositories import UserRepository
from app.schemas.requests.auth import AuthIn, AuthLogin
from app.schemas.responses.auth import AuthOut
from app.schemas.responses.user import UserOut
from core.controller import BaseController
from core.exceptions import DuplicateValueException, UnauthorizedException
from core.security import JWTService, PasswordService


class AuthController(BaseController[DBUser]):
    def __init__(
        self, repository: UserRepository, jwt: JWTService, password: PasswordService
    ) -> None:
        super().__init__(DBUser, repository)
        self.repository: UserRepository = repository
        self.jwt: JWTService = jwt
        self.password: PasswordService = password

    async def register(self, data: AuthIn) -> AuthOut:
        if await self.repository.get_by_email(data.email):
            raise DuplicateValueException()
        if await self.repository.get_by_username(data.username):
            raise DuplicateValueException()

        hashed_password = self.password.hash_password(data.password)

        user = await self.repository.create(
            {
                "email": data.email,
                "username": data.username,
                "password": hashed_password,
            }
        )

        await self.commit()

        token = self.jwt.build_token_pair(
            str(user.uid),
            extra_claims={"user": {"username": user.username, "email": user.email}},
        )

        return AuthOut(
            token=token,
            user=UserOut.model_validate(user),
        )

    async def login(self, data: AuthLogin) -> AuthOut:

        user = await self.repository.get_by_username_or_email(data.username_or_email)

        if user is None:
            raise UnauthorizedException(
                message="Invalid credentials",
                error_code="INVALID_CREDENTIALS",
            )

        if user.password and not self.password.verify_password(
            user.password, data.password
        ):
            raise UnauthorizedException(
                message="Invalid credentials",
                error_code="INVALID_CREDENTIALS",
            )

        token = self.jwt.build_token_pair(
            str(user.uid),
            extra_claims={"user": {"username": user.username, "email": user.email}},
        )

        return AuthOut(token=token, user=UserOut.model_validate(user))
