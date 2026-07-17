# Transaction domain model and MongoDB serialization helpers.

from decimal import Decimal
from datetime import datetime, timezone


class Transaction:
    # Represents a deposit or withdrawal for one account.
    # New transactions receive a timezone-aware UTC timestamp.

    #constructor for initialization of a transaction
    def __init__(self, tranType, amount, accountId, createdAt=None) :
        self.__tranType = tranType
        self.__amount = Decimal(str(amount))
        self.__accountId = accountId
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

    #method for encapsulation and get timestamp for transaction creation
    def getCreatedAt(self):
        return self.__createdAt
    
    #method to convert transaction object into storable text object for mongoDb
    def to_dict(self) -> dict:
        # Serialize using the transaction collection's field names.
        return {
            "account_id": self.__accountId,
            "type": self.__tranType,
            "amount": float(self.__amount),
            "created_at": self.__createdAt,
        }

    #method for conversion of mongoDb text object back to transaction object
    @classmethod
    def from_dict(cls, dc: dict) -> "Transaction":
        # Build a transaction from a MongoDB document.
        return cls(
            tranType=dc["type"],
            amount=dc["amount"],
            accountId=dc["account_id"],
            createdAt=dc.get("created_at"),
        )
