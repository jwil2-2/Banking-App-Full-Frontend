
from decimal import Decimal

#Class for creation of account objects
#including associated userId so that each account is connected back to a user
class Account() :

    

    #Initialize account
    def __init__(self, userId, accountType, balance=None, accountId="") :

        #Storage of account id, balance, account type, and associated user id
        self.__accountId = accountId
        self.__balance = Decimal(str(balance)) if balance is not None else Decimal("0.00")
        self.__accountType = accountType
        self.__userId = userId

    
    
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
    
    
    #method for encapsulation and showcase of current account details
    def getAccountDetails(self):
        return {
            "Account ID": self.__accountId,
            "Account Type": self.__accountType,
            "User ID": self.__userId,
            "Balance": self.__balance,
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
    
    

    
   