from decimal import Decimal

from ..db import accounts_collection
from bson import ObjectId



#Class responsible for account data management with mongoDb calls
class AccountRepository:

    #method to call mongoDb for insertino of banking account
    async def create(self, accountDc: dict) -> str:
        result = await accounts_collection.insert_one(accountDc)
        return str(result.inserted_id)
    
    #method to return mongoDb bank acount by accountId
    async def getById(self, accountId: str) -> dict | None:
        return await accounts_collection.find_one({"_id": ObjectId(accountId)})
    
    #method to call mongoDb ot find all banking accounts for user
    async def getAllForUser(self, userId:str) -> list[dict]:
        cursor = accounts_collection.find({"userId": userId})
        return [dc async for dc in cursor]
    
    #mtehod to update balance in mongoDb for users specific account
    async def updateBalance(self, accountId:str, delta: Decimal) -> None:
        await accounts_collection.update_one(
            {"_id": ObjectId(accountId)},
             {"$inc": {"balance": float(delta)}}
        )
    
    #method to add transaction to associated with accounntId to mongo Db
    async def addTransaction(self, accountId: str, transactionDc: dict) -> None:
        await accounts_collection.update_one(
            {"_id": ObjectId(accountId)},
            {"$push": {"transactions": transactionDc}}
        )
   