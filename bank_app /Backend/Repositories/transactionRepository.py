from ..db import transactions_collection
from ..transaction import Transaction

#Class responsible for transaction data management with mongoDb calls
class TransactionRepository:

    #call to mongoDB to create transaction for associated account
    async def create(self, transaction_dc: dict) -> str:
        result = await transactions_collection.insert_one(transaction_dc)
        return str(result.inserted_id)

    #call to mongoDB to return all transactions for associated bank account
    async def getAllForAccount(self, accountId: str) -> list[Transaction]:
        cursor = transactions_collection.find({"account_id": accountId}).sort("created_at", 1)
        return [Transaction.from_dict(dc) async for dc in cursor]