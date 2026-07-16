
from ..db import users_collection

#class resposnible for user data management with calls to mongoDb
class UserRepository:
    
    #method to call mongoDb for user creation
    async def create(self, user_dc: dict) -> str:
        result = await users_collection.insert_one(user_dc)
        return str(result.inserted_id)
     
    #method to get all users from mongoDb
    #do some editing so admin only gets this functionality
    async def getAllUsers(self) -> list[dict]:
        cursor = users_collection.find({})
        return [dc async for dc in cursor]