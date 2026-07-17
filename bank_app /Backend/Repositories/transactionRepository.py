# MongoDB persistence operations for account transactions.

from ..db import transactions_collection
from ..transaction import Transaction

class TransactionRepository:
    # Stores transaction documents and rebuilds transaction models.

    async def create(self, transaction_dc: dict) -> str:
        # Insert a transaction and return its generated ID as a string.
        result = await transactions_collection.insert_one(transaction_dc)
        return str(result.inserted_id)

    async def getAllForAccount(self, accountId: str) -> list[Transaction]:
        # Return an account's transactions ordered oldest to newest.
        cursor = transactions_collection.find({"account_id": accountId}).sort("created_at", 1)
        return [Transaction.from_dict(dc) async for dc in cursor]