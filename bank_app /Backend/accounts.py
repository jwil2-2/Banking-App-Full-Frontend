
from decimal import Decimal
from .user import User
from .transaction import Transaction

#Class for creation of account objects
#including associated userId so that each account is connected back to a user
class Account() :

    #gloabal counter for account Id numbers
    idCounter = 1

    #Initialize account
    def __init__(self, userId, accountType, balance=None, accountId="") :

        #Storage of account id, balance, account type, associated user id, and creation and storage of empty transaction list
        self.__accountId = accountId
        self.__balance = Decimal(str(balance)) if balance is not None else Decimal("0.00")
        self.__accountType = accountType
        self.__userId = userId

        self.__transactions = []

        #increment of counter for unique account ids across user session
        Account.idCounter += 1
    
    #method for encapsulation and returning balance
    def getBalance(self) :
        return self.__balance
    
    #pmethod for encapsulation and setting balance
    def setBalance(self, amount) :
        self.__balance += amount
    
    #method for encapsulation and returning account type
    def getAccType(self) :
        return self.__accountType
    
    #method for returning userId of account
    def getUserId(self) :
        return self.__userId

    #method for returning userId of account
    def getAccountId(self) :
        return self.__accountId
    
    
    #method for encapsulation and addition of transactions to the account in use
    def addTransaction(self, transaction) :
        self.__transactions.append(transaction)
    
    #mthod for encapsulation and return of transaction list to be shown to the user
    def getTransactions(self) :
        return self.__transactions
    
    #method for encapsulation and showcase of current account details
    def getAccountDetails(self):
        return {
            "Account ID": self.__accountId,
            "Account Type": self.__accountType,
            "User ID": self.__userId,
            "Balance": self.__balance,
            "Transactions": self.__transactions,
        }
    
    def setAccountId(self, account_id):
        # called once, after Mongo assigns the real _id on insert
        self.__accountId = account_id

    #method for conversion of account object to storable strings for mongo
    def toDict(self) -> dict:
        return {
            "userId": self.__userId,
            "accountType": self.__accountType,
            "balance": float(self.__balance),
        }
    
    #mthod for conversion back into account object
    @classmethod
    def fromDict(cls, dc: dict) -> "Account":
        return cls(
            userId=dc["userId"],
            accountType=dc["accountType"],
            balance=dc["balance"],
            accountId=str(dc["_id"]),
        )
    
    

    
   