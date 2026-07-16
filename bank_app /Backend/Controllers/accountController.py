from fastapi import APIRouter, HTTPException
from decimal import Decimal
from pydantic import BaseModel, Field
from ..Services.accountService import AccountService
from ..Repositories.accountRepository import AccountRepository
from ..Repositories.transactionRepository import TransactionRepository

router = APIRouter(prefix="/api/accounts", tags=["accounts"])
_accountRepository = AccountRepository()
_transactionRepository = TransactionRepository()
_accountService = AccountService(_accountRepository, _transactionRepository)

# Class that actually creates and calls API endpoints which initiates CRUD
class AccountController:

    #class that defines and validates response data when client creates, fetches or updates account data
    class AccountOut(BaseModel):
        id: str
        account_type: str
        user_id: str
        balance: Decimal

    class TransactionOut(BaseModel):
        account_id: str
        type: str
        amount: Decimal
        created_at: str | None = None

    class AccountDetailOut(AccountOut):
        transactions: list["AccountController.TransactionOut"]
    
    #class that defines and validates when client sends request to create new account
    class CreateAccountRequest(BaseModel):
        account_type: str = Field(pattern="^(Checking|Savings)$")

    class AmountRequest(BaseModel):
        amount: Decimal = Field(gt=0)

    @staticmethod
    def _resolve_user_id(user_id: str | None = None, userId: str | None = None) -> str:
        resolved_user_id = user_id or userId
        if not resolved_user_id:
            raise HTTPException(status_code=400, detail="user id is required")
        return resolved_user_id

    # Api to read and list all of users banking accounts 
    @router.get("", response_model=list[AccountOut])
    async def listAccounts(user_id: str | None = None, userId: str | None = None):
        # TEMPORARY: once login/JWT exists, replace `user_id: str` query param
        # with `user: User = Depends(get_current_user)` and use user.getUserId()
        resolved_user_id = AccountController._resolve_user_id(user_id, userId)
        accounts = await _accountService.getAllAccounts(resolved_user_id)
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
    async def create_account(payload: CreateAccountRequest, user_id: str | None = None, userId: str | None = None):
    # TEMPORARY: user_id as a query param until auth exists (see list_accounts note)
        resolved_user_id = AccountController._resolve_user_id(user_id, userId)
        account = await _accountService.createAccount(resolved_user_id, payload.account_type)
        account_id = account.getAccountId()
        if not account_id:
            raise ValueError("Account id missing after creation")
        return AccountController.AccountOut(
            id=str(account_id),
            account_type=account.getAccType(),
            user_id=account.getUserId(),
            balance=account.getBalance(),
            )

    # api calls to return acount details for user logged in
    @router.get("/{account_id}", response_model=AccountDetailOut)
    async def get_account_details(account_id: str):
        try:
            details = await _accountService.getAccountDetails(account_id)
        except ValueError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc

        return AccountController.AccountDetailOut(
            id=details["Account ID"],
            account_type=details["Account Type"],
            user_id=details["User ID"],
            balance=details["Balance"],
            transactions=[
                AccountController.TransactionOut(
                    account_id=transaction.getAccountId(),
                    type=transaction.getTranType(),
                    amount=transaction.getAmount(),
                    created_at=str(transaction.getCreatedAt()) if transaction.getCreatedAt() else None,
                )
                for transaction in details.get("Transactions", [])
            ],
        )

    # apit call to get transactions associated with bank account
    @router.get("/{account_id}/transactions", response_model=list[TransactionOut])
    async def get_transactions(account_id: str):
        try:
            transactions = await _accountService.getTransactionHistory(account_id)
        except ValueError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc

        return [
            AccountController.TransactionOut(
                account_id=transaction.getAccountId(),
                type=transaction.getTranType(),
                amount=transaction.getAmount(),
                created_at=str(transaction.getCreatedAt()) if transaction.getCreatedAt() else None,
            )
            for transaction in transactions
        ]

    #api call to deposit money into associated bank account
    @router.post("/{account_id}/deposit", response_model=AccountOut)
    async def deposit(account_id: str, payload: AmountRequest):
        try:
            account = await _accountService.deposit(account_id, payload.amount)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

        return AccountController.AccountOut(
            id=str(account.getAccountId()),
            account_type=account.getAccType(),
            user_id=account.getUserId(),
            balance=account.getBalance(),
        )

    #api call to withdraw money from asssociated bank account
    @router.post("/{account_id}/withdraw", response_model=AccountOut)
    async def withdraw(account_id: str, payload: AmountRequest):
        try:
            account = await _accountService.withdraw(account_id, payload.amount)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

        return AccountController.AccountOut(
            id=str(account.getAccountId()),
            account_type=account.getAccType(),
            user_id=account.getUserId(),
            balance=account.getBalance(),
        )