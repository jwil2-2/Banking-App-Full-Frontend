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
