from fastapi import APIRouter
from decimal import Decimal
from pydantic import BaseModel, Field
from ..Services.userService import UserService
from ..Repositories.accountRepository import AccountRepository

router = APIRouter(prefix="/api/users", tags=["users"])
_userRepository = AccountRepository()
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


    #initialization of Account service to use
    def __init__(self, service: UserService):
        self.service = service

    # Api to create new banking account for user
    @router.post("", response_model=UserOut, status_code=201)
    async def create_account(payload: CreateUserRequest):
    # TEMPORARY: user_id as a query param until auth exists (see list_accounts note)
        user = await _userService.createUser(payload.name, payload.email, payload.password, payload.role)
        return UserController.UserOut(
            name=user.getName(),
            email=user.getEmail(),
            role=user.getRole(),
            )