from ..Repositories.userRepository import UserRepository
from ..user import User, AdminUser



class UserService:

     #initialization of repository to use for needed retrieval of data from mongoDb
    def __init__(self, repository: UserRepository):
        self.repository = repository

    #starts user creation process with model call, then associated calls to repository
    #for mongoDb storage
    async def createUser(self, name, email, password, role):
        user = AdminUser(name, email, password) if role == "admin" else User(name, email, password)
        userId = await self.repository.create(user.toDict())
        user.setUserId(userId)
        return user
    
    #starts Admin creation process with model call, then associated calls to repository
    #for mongoDb storage
    async def createAdmin(self, name, email, password, role):
        user = AdminUser(name, email, password)
        userId = await self.repository.create(user.toDict())
        user.setUserId(userId)
        return user

    # begins login process for the user
    async def loginUser(self, email: str, password: str):
        user_dc = await self.repository.getByEmail(email)
        if not user_dc:
            raise ValueError("Invalid email or password")

        user = User.fromDict(user_dc)
        if user.getPassword() != password:
            raise ValueError("Invalid email or password")

        return user