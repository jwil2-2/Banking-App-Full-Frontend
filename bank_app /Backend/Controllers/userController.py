from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from ..Repositories.userRepository import UserRepository
from ..Services.userService import UserService

router = APIRouter(prefix="/api/users", tags=["users"])
_userRepository = UserRepository()
_userService = UserService(_userRepository)

#Class that creates and uses API endpoints to initiate CRUD operations
class UserController:

    #class that defines and validates response data when client creates, fetches or updates account data
    class UserOut(BaseModel):
        id: str
        name: str
        email: str
        role: str

    #class that defines and validates when client sends request to create new account
    class CreateUserRequest(BaseModel):
        name: str
        email: str
        password: str
        role: str = Field(pattern="^(user|admin)$")

    class LoginRequest(BaseModel):
        email: str
        password: str


    #initialization of Account service to use
    def __init__(self, service: UserService):
        self.service = service

    # Api to create new banking account for user
    @router.post("", response_model=UserOut, status_code=201)
    async def create_user(payload: CreateUserRequest):
        user = await _userService.createUser(payload.name, payload.email, payload.password, payload.role)
        return UserController.UserOut(
            id=user.getUserId(),
            name=user.getName(),
            email=user.getEmail(),
            role=user.getRole(),
            )

    #api call to  login created user with correct credentials pprovided
    @router.post("/login", response_model=UserOut)
    async def login(payload: LoginRequest):
        try:
            user = await _userService.loginUser(payload.email, payload.password)
        except ValueError as exc:
            raise HTTPException(status_code=401, detail=str(exc)) from exc

        return UserController.UserOut(
            id=user.getUserId(),
            name=user.getName(),
            email=user.getEmail(),
            role=user.getRole(),
        )