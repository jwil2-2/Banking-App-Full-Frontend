# Account domain model and MongoDB serialization helpers.

from decimal import Decimal

class Account:
    # Represents one user-owned checking or savings account.
    # Balances use Decimal in the app and floats in MongoDB documents.

    def __init__(self, userId, accountType, balance=None, accountId=""):
        self.__accountId = accountId
        self.__balance = Decimal(str(balance)) if balance is not None else Decimal("0.00")
        self.__accountType = accountType
        self.__userId = userId

    
    
    #method for encapsulation and returning balance
    def getBalance(self) :
        return self.__balance
    
    def setBalance(self, amount):
        # Apply a positive or negative delta to the current balance.
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
    
    
    #method for encapsulation and showcase of current account details
    def getAccountDetails(self):
        # Return the service-layer account detail structure.
        return {
            "Account ID": self.__accountId,
            "Account Type": self.__accountType,
            "User ID": self.__userId,
            "Balance": self.__balance,
        }
    
    def setAccountId(self, account_id):
        # Assign the ID generated after a MongoDB insert.
        self.__accountId = account_id

    #method for conversion of account object to storable strings for mongo
    def toDict(self) -> dict:
        # Serialize the account for MongoDB, excluding its generated ID.
        return {
            "userId": self.__userId,
            "accountType": self.__accountType,
            "balance": float(self.__balance),
        }
    
    #method for conversion back into account object
    @classmethod
    def fromDict(cls, dc: dict) -> "Account":
        # Build an account from a MongoDB document.
        return cls(
            userId=dc["userId"],
            accountType=dc["accountType"],
            balance=dc["balance"],
            accountId=str(dc["_id"]),
        )