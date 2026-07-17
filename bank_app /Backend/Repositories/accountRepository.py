# MongoDB persistence operations for bank accounts.

from decimal import Decimal

from ..db import accounts_collection
from bson import ObjectId



#Class responsible for account data management with mongoDb calls
class AccountRepository:
    # Stores and retrieves account documents without business logic.

    #method to call mongoDb for insertino of banking account
    async def create(self, accountDc: dict) -> str:
        # Insert an account and return its generated ID as a string.
        result = await accounts_collection.insert_one(accountDc)
        return str(result.inserted_id)
    
    #method to return mongoDb bank acount by accountId
    async def getById(self, accountId: str) -> dict | None:
        # Find an account by a valid MongoDB ObjectId string.
        return await accounts_collection.find_one({"_id": ObjectId(accountId)})
    
    #method to call mongoDb ot find all banking accounts for user
    async def getAllForUser(self, userId:str) -> list[dict]:
        # Return all account documents belonging to one user.
        cursor = accounts_collection.find({"userId": userId})
        return [dc async for dc in cursor]
    
    #mtehod to update balance in mongoDb for users specific account
    async def updateBalance(self, accountId:str, delta: Decimal) -> None:
        # Atomically increment an account balance by delta.
        await accounts_collection.update_one(
            {"_id": ObjectId(accountId)},
             {"$inc": {"balance": float(delta)}}
        )
   