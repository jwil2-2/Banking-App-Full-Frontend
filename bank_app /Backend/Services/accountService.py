from ..accounts import Account
from ..Repositories.accountRepository import AccountRepository
from ..Repositories.transactionRepository import TransactionRepository
from ..user import User
from ..transaction import Transaction
from decimal import Decimal

#creating instance of account repository class to use its associated methods
repository = AccountRepository

#Class used to service application and call needed methods when creating and managing accounts
#and any additional logic
class AccountService:

    #initialization of repository to use for needed retrieval of data from mongoDb
    def __init__(self, repository: AccountRepository, transactionRepository: TransactionRepository):
        self.repository = repository
        self.transactionRepository = transactionRepository

    #starts account creation process with model call, then associated calls to repository
    #for mongoDb storage
    async def createAccount(self, userId, accountType: str):
        account = Account(userId, accountType)
        accountId = await self.repository.create(account.toDict())
        if not accountId:
            raise RuntimeError("Account repository did not return an id")
        account.setAccountId(accountId)
        if not account.getAccountId():
            raise RuntimeError("Account id was not assigned")
        return account
    
    #starts process of returning all account for user with assosciated call to repository
    #which then calls mongoDb
    async def getAllAccounts(self, userId: str) -> list[Account]:
        dcs = await self.repository.getAllForUser(userId)
        return [Account.fromDict(d) for d in dcs]

    # method to start process of retrieving account by specific id in repository
    async def getAccountById(self, accountId: str) -> Account:
        account_dc = await self.repository.getById(accountId)
        if not account_dc:
            raise ValueError("Account not found")
        return Account.fromDict(account_dc)

    #mthod to start process of getting account details for user by accountid
    async def getAccountDetails(self, accountId: str) -> dict:
        account = await self.getAccountById(accountId)
        transactions = await self.getTransactionHistory(accountId)
        details = account.getAccountDetails()
        details["Transactions"] = transactions
        return details

    #method to start process of depositing money into associated account in repositories
    #as well keeping track of transaction
    async def deposit(self, accountId: str, amount: Decimal) -> Account:
        if amount <= 0:
            raise ValueError("Deposit amount must be greater than zero")

        account = await self.getAccountById(accountId)
        transaction = Transaction("Deposit", amount, accountId)
        await self.repository.updateBalance(accountId, amount)
        await self.transactionRepository.create(transaction.to_dict())
        account.setBalance(amount)
        return account

    #method to start process of withdrawing money from associated account in repositories
    #as well keeping track of transaction
    async def withdraw(self, accountId: str, amount: Decimal) -> Account:
        if amount <= 0:
            raise ValueError("Withdrawal amount must be greater than zero")

        account = await self.getAccountById(accountId)
        if account.getBalance() < amount:
            raise ValueError("Not enough money in account")

        transaction = Transaction("Withdrawal", amount, accountId)
        await self.repository.updateBalance(accountId, -amount)
        await self.transactionRepository.create(transaction.to_dict())
        account.setBalance(-amount)
        return account

    #method to start process of recieving transaction history of associated account in repository
    async def getTransactionHistory(self, accountId: str) -> list[Transaction]:
        return await self.transactionRepository.getAllForAccount(accountId)
