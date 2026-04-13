from typing import Callable, List

from app.models.user import DBUserRole
from core.dependencies.user import CurrentUserDep


def require_roles(required_roles: List[DBUserRole]) -> Callable:
    """Dependency factory for role-based access control."""

    async def check_roles(current_user: CurrentUserDep):

        if current_user.role not in required_roles:
            raise PermissionError("User does not have the required permission.")

        return current_user

    return check_roles
