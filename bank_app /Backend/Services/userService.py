from ..Repositories.userRepository import UserRepository
from ..user import User, AdminUser



class UserService:

     #initialization of repository to use for needed retrieval of data from mongoDb
    def __init__(self, repository: UserRepository):
        self.repository = repository

    #starts user creation process with model call, then associated calls to repository
    #for mongoDb storage
    async def createUser(self, name, email, password, role):
        user = User(name, email, password)
        userId = await self.repository.create(user.toDict())
        user._id = userId
        return user
    
    #starts Admin creation process with model call, then associated calls to repository
    #for mongoDb storage
    async def createAdmin(self, name, email, password, role):
        user = AdminUser(name, email, password)
        userId = await self.repository.create(user.toDict())
        user._id = userId
        return user