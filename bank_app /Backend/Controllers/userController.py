# User registration, login, profile, and admin-management API routes.
# Registration/login are public; management routes require the admin role.

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from ..Repositories.userRepository import UserRepository
from ..Services.userService import UserService
from ..auth.dependencies import get_current_user, require_roles
from ..auth.jwt_utils import create_access_token
from ..auth.schemas import CurrentUser

router = APIRouter(prefix="/api/users", tags=["users"])
_userRepository = UserRepository()
_userService = UserService(_userRepository)


def _user_out(user) -> "UserController.UserOut":
    # Convert the domain user model into its public response shape.
    return UserController.UserOut(
        id=user.getUserId(),
        name=user.getName(),
        email=user.getEmail(),
        role=user.getRole(),
    )


def _auth_response(user) -> "UserController.AuthResponse":
    # Issue an access token and pair it with the authenticated user.
    token = create_access_token(
        user_id=user.getUserId(),
        role=user.getRole(),
        email=user.getEmail(),
    )
    return UserController.AuthResponse(
        access_token=token,
        user=_user_out(user),
    )


class UserController:
    # Namespace for user API schemas and route handlers.

    class UserOut(BaseModel):
        # Public user fields; passwords are never returned.

        id: str
        name: str
        email: str
        role: str

    class AuthResponse(BaseModel):
        # Successful authentication response consumed by the frontend.

        access_token: str
        token_type: str = "bearer"
        user: "UserController.UserOut"

    class CreateUserRequest(BaseModel):
        # Public registration payload; new users always receive the user role.

        name: str
        email: str
        password: str

    class AdminCreateUserRequest(CreateUserRequest):
        # Admin-only user creation payload with an explicit role.

        role: str = Field(pattern="^(user|admin)$")

    class LoginRequest(BaseModel):
        email: str
        password: str

    @router.post("", response_model=AuthResponse, status_code=201)
    async def create_user(payload: CreateUserRequest):
        # Register a standard user and immediately issue an access token.
        user = await _userService.createUser(payload.name, payload.email, payload.password, "user")
        return _auth_response(user)

    @router.post("/admin", response_model=UserOut, status_code=201)
    async def create_user_as_admin(
        payload: AdminCreateUserRequest,
        _: CurrentUser = Depends(require_roles("admin")),
    ):
        # Create a user or admin; callable only by an authenticated admin.
        user = await _userService.createUser(payload.name, payload.email, payload.password, payload.role)
        return _user_out(user)

    @router.post("/login", response_model=AuthResponse)
    async def login(payload: LoginRequest):
        # Validate credentials and return a new access token.
        try:
            user = await _userService.loginUser(payload.email, payload.password)
        except ValueError as exc:
            raise HTTPException(status_code=401, detail=str(exc)) from exc

        return _auth_response(user)

    @router.get("/me", response_model=UserOut)
    async def get_me(current_user: CurrentUser = Depends(get_current_user)):
        # Return the authenticated user's current database profile.
        return UserController.UserOut(
            id=current_user.id,
            name=current_user.name,
            email=current_user.email,
            role=current_user.role,
        )

    @router.get("", response_model=list[UserOut])
    async def list_users(_: CurrentUser = Depends(require_roles("admin"))):
        # Return all users to administrators.
        users = await _userService.getAllUsers()
        return [_user_out(user) for user in users]
