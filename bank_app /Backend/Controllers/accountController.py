# Authenticated account, balance, and transaction API routes.
# Users access their own accounts; admins may access any user's accounts.

from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from ..Repositories.accountRepository import AccountRepository
from ..Repositories.transactionRepository import TransactionRepository
from ..Services.accountService import AccountService
from ..auth.dependencies import get_current_user
from ..auth.schemas import CurrentUser

router = APIRouter(prefix="/api/accounts", tags=["accounts"])
_accountRepository = AccountRepository()
_transactionRepository = TransactionRepository()
_accountService = AccountService(_accountRepository, _transactionRepository)


async def _ensure_account_access(account_id: str, current_user: CurrentUser):
    # Load an account and enforce owner-or-admin access.
    # Missing accounts return 404 and unauthorized access returns 403.
    try:
        account = await _accountService.getAccountById(account_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    if current_user.role != "admin" and account.getUserId() != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this account")

    return account


class AccountController:
    # Namespace for account API schemas and protected route handlers.

    class AccountOut(BaseModel):
        # Summary returned after account reads and balance changes.

        id: str
        account_type: str
        user_id: str
        balance: Decimal

    class TransactionOut(BaseModel):
        # Serialized transaction returned to API clients.

        account_id: str
        type: str
        amount: Decimal
        created_at: str | None = None

    class AccountDetailOut(AccountOut):
        transactions: list["AccountController.TransactionOut"]

    class CreateAccountRequest(BaseModel):
        account_type: str = Field(pattern="^(Checking|Savings)$")

    class AmountRequest(BaseModel):
        amount: Decimal = Field(gt=0)

    @router.get("", response_model=list[AccountOut])
    async def listAccounts(
        current_user: CurrentUser = Depends(get_current_user),
        userId: str | None = None,
    ):
        # List the current user's accounts, or an admin-selected user's.
        target_user_id = current_user.id
        if current_user.role == "admin" and userId:
            target_user_id = userId

        accounts = await _accountService.getAllAccounts(target_user_id)
        return [
            AccountController.AccountOut(
                id=a.getAccountId(),
                account_type=a.getAccType(),
                user_id=a.getUserId(),
                balance=a.getBalance(),
            )
            for a in accounts
        ]

    @router.post("", response_model=AccountOut, status_code=201)
    async def create_account(
        payload: CreateAccountRequest,
        current_user: CurrentUser = Depends(get_current_user),
    ):
        # Create an account owned by the authenticated user.
        account = await _accountService.createAccount(current_user.id, payload.account_type)
        account_id = account.getAccountId()
        if not account_id:
            raise ValueError("Account id missing after creation")
        return AccountController.AccountOut(
            id=str(account_id),
            account_type=account.getAccType(),
            user_id=account.getUserId(),
            balance=account.getBalance(),
        )

    @router.get("/{account_id}", response_model=AccountDetailOut)
    async def get_account_details(
        account_id: str,
        current_user: CurrentUser = Depends(get_current_user),
    ):
        # Return account metadata and transactions after access checks.
        await _ensure_account_access(account_id, current_user)

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

    @router.get("/{account_id}/transactions", response_model=list[TransactionOut])
    async def get_transactions(
        account_id: str,
        current_user: CurrentUser = Depends(get_current_user),
    ):
        # Return authorized account transactions in chronological order.
        await _ensure_account_access(account_id, current_user)

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

    @router.post("/{account_id}/deposit", response_model=AccountOut)
    async def deposit(
        account_id: str,
        payload: AmountRequest,
        current_user: CurrentUser = Depends(get_current_user),
    ):
        # Deposit a positive amount into an authorized account.
        await _ensure_account_access(account_id, current_user)

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

    @router.post("/{account_id}/withdraw", response_model=AccountOut)
    async def withdraw(
        account_id: str,
        payload: AmountRequest,
        current_user: CurrentUser = Depends(get_current_user),
    ):
        # Withdraw available funds from an authorized account.
        await _ensure_account_access(account_id, current_user)

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
