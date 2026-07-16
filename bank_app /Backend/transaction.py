# Class to keep up with user transactions in bank app
from decimal import Decimal
from datetime import datetime, timezone


class Transaction:

    #constructor for initialization of a transaction
    def __init__(self, tranType, amount, accountId, transactionId=None, createdAt=None) :
        self.__tranType = tranType
        self.__amount = Decimal(str(amount))
        self.__accountId = accountId
        self.__transactionId = transactionId
        self.__createdAt = createdAt or datetime.now(timezone.utc)

    #method for encapsulation and returning transaction type
    def getTranType(self):
        return self.__tranType
    
    #method for encapsulation and returning amount
    def getAmount(self):
        return self.__amount
    
    #method for encapsulation and returning associated account id for transaction
    def getAccountId(self):
        return self.__accountId

    #method for encapsulation and returning transaction id
    def getTransactionId(self):
        return self.__transactionId

    #method for encapsulation and setting transaction id
    def setTransactionId(self, transaction_id):
        # called once, after Mongo assigns the real _id on insert
        self.__transactionId = transaction_id

    #method for encapsulation and get timestamp for transaction creation
    def getCreatedAt(self):
        return self.__createdAt
    
    #method to convert transaction object into storable text object for mongoDb
    def to_dict(self) -> dict:
        return {
            "account_id": self.__accountId,
            "type": self.__tranType,
            "amount": float(self.__amount),
            "created_at": self.__createdAt,
        }

    #method for conversion of mongoDb text object back to transaction object
    @classmethod
    def from_dict(cls, dc: dict) -> "Transaction":
        return cls(
            tranType=dc["type"],
            amount=dc["amount"],
            account_id=dc["account_id"],
            transaction_id=str(dc["_id"]),
            created_at=dc.get("created_at"),
        )
