# FastAPI dependencies for Bearer-token authentication and role checks.

from typing import Callable

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from ..Repositories.userRepository import UserRepository
from ..user import User
from .jwt_utils import decode_access_token
from .schemas import CurrentUser

_bearer_scheme = HTTPBearer(auto_error=False)
_user_repository = UserRepository()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer_scheme),
) -> CurrentUser:
    # Authenticate a Bearer token and return the current database identity.
    # Reload user fields from MongoDB so role changes and deletions take effect
    # without waiting for an otherwise valid token to expire.
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        payload = decode_access_token(credentials.credentials)
    except jwt.PyJWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")

    user_dc = await _user_repository.getById(user_id)
    if not user_dc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    user = User.fromDict(user_dc)
    return CurrentUser(
        id=user.getUserId(),
        name=user.getName(),
        email=user.getEmail(),
        role=user.getRole(),
    )


def require_roles(*allowed_roles: str) -> Callable:
    # Build a dependency that permits only the listed roles.
    # Authentication failures return 401; insufficient roles return 403.
    async def _checker(current_user: CurrentUser = Depends(get_current_user)) -> CurrentUser:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )
        return current_user

    return _checker
