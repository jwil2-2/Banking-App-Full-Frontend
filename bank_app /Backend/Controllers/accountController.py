from fastapi import APIRouter
from decimal import Decimal
from pydantic import BaseModel, Field
from ..Services.accountService import AccountService
from ..Repositories.accountRepository import AccountRepository

router = APIRouter(prefix="/api/accounts", tags=["accounts"])
_accountRepository = AccountRepository()
_accountService = AccountService(_accountRepository)

# Class that actually creates and calls API endpoints which initiates CRUD
class AccountController:

    #class that defines and validates response data when client creates, fetches or updates account data
    class AccountOut(BaseModel):
        id: str
        account_type: str
        user_id: str
        balance: Decimal
    
    #class that defines and validates when client sends request to create new account
    class CreateAccountRequest(BaseModel):
        account_type: str = Field(pattern="^(Checking|Savings)$")

    #initialization of Account service to use
    def __init__(self, service: AccountService):
        self.service = service

    #setup of app api
    #app = FastAPI()

    # Api to read and list all of users banking accounts 
    @router.get("", response_model=list[AccountOut])
    async def listAccounts(userId: str):
        # TEMPORARY: once login/JWT exists, replace `user_id: str` query param
        # with `user: User = Depends(get_current_user)` and use user.getUserId()
        accounts = await _accountService.getAllAccounts(userId)
        return [
            AccountController.AccountOut(
                id=a.getAccountId(),
                account_type=a.getAccType(),
                user_id=a.getUserId(),
                balance=a.getBalance(),
            )
            for a in accounts
        ]
    
    # Api to create new banking account for user
    @router.post("", response_model=AccountOut, status_code=201)
    async def create_account(payload: CreateAccountRequest, user_id: str):
    # TEMPORARY: user_id as a query param until auth exists (see list_accounts note)
        account = await _accountService.createAccount(user_id, payload.account_type)
        return AccountController.AccountOut(
            id=account.getAccountId(),
            account_type=account.getAccType(),
            user_id=account.getUserId(),
            balance=account.getBalance(),
            )