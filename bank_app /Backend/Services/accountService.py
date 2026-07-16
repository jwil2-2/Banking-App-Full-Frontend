from ..accounts import Account
from ..Repositories.accountRepository import AccountRepository
from ..user import User

#creating instance of account repository class to use its associated methods
repository = AccountRepository

#Class used to service application and call needed methods when creating and managing accounts
#and any additional logic
class AccountService:

    #initialization of repository to use for needed retrieval of data from mongoDb
    def __init__(self, repository: AccountRepository):
        self.repository = repository

    #starts account creation process with model call, then associated calls to repository
    #for mongoDb storage
    async def createAccount(self, user: User, accountType: str):
        account = Account(user.getUserId(), accountType)
        accountId = await self.repository.create(account.toDict())
        account._id = accountId
        return account
    
    #starts process of returning all account for user with assosciated call to repository
    #which then calls mongoDb
    async def getAllAccounts(self, userId: str) -> list[Account]:
        dcs = await self.repository.getAllForUser(userId)
        return [Account.fromDict(d) for d in dcs]
