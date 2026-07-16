from bson import ObjectId

from ..db import users_collection

#class resposnible for user data management with calls to mongoDb
class UserRepository:
    
    #method to call mongoDb for user creation
    async def create(self, user_dc: dict) -> str:
        result = await users_collection.insert_one(user_dc)
        return str(result.inserted_id)

    #call to mongoDb to get user by associated email
    async def getByEmail(self, email: str) -> dict | None:
        return await users_collection.find_one({"email": email})

    #call to mongoDb to get user by specific id
    async def getById(self, userId: str) -> dict | None:
        return await users_collection.find_one({"_id": ObjectId(userId)})

    #method to get all users from mongoDb
    async def getAllUsers(self) -> list[dict]:
        cursor = users_collection.find({})
        return [dc async for dc in cursor]
