# MongoDB persistence operations for users.

from bson import ObjectId

from ..db import users_collection

class UserRepository:
    # Stores and queries user documents without authentication logic.
    
    async def create(self, user_dc: dict) -> str:
        # Insert a user and return its generated ID as a string.
        result = await users_collection.insert_one(user_dc)
        return str(result.inserted_id)

    async def getByEmail(self, email: str) -> dict | None:
        # Find one user by email address.
        return await users_collection.find_one({"email": email})

    async def getById(self, userId: str) -> dict | None:
        # Find one user by a valid MongoDB ObjectId string.
        return await users_collection.find_one({"_id": ObjectId(userId)})

    async def getAllUsers(self) -> list[dict]:
        # Return every user document; callers handle authorization.
        cursor = users_collection.find({})
        return [dc async for dc in cursor]
