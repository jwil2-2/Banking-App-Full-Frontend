from ..Repositories.userRepository import UserRepository
from ..auth.passwords import hash_password, verify_password
from ..user import User, AdminUser


class UserService:

     #initialization of repository to use for needed retrieval of data from mongoDb
    def __init__(self, repository: UserRepository):
        self.repository = repository

    #starts user creation process with model call, then associated calls to repository
    #for mongoDb storage
    async def createUser(self, name, email, password, role):
        user = AdminUser(name, email, password) if role == "admin" else User(name, email, password)
        user_dc = user.toDict()
        user_dc["password"] = hash_password(password)
        userId = await self.repository.create(user_dc)
        user.setUserId(userId)
        return user

    async def getAllUsers(self) -> list[User]:
        user_docs = await self.repository.getAllUsers()
        return [User.fromDict(dc) for dc in user_docs]

    async def getUserById(self, user_id: str) -> User:
        user_dc = await self.repository.getById(user_id)
        if not user_dc:
            raise ValueError("User not found")
        return User.fromDict(user_dc)

    # begins login process for the user
    async def loginUser(self, email: str, password: str):
        user_dc = await self.repository.getByEmail(email)
        if not user_dc:
            raise ValueError("Invalid email or password")

        if not verify_password(password, user_dc["password"]):
            raise ValueError("Invalid email or password")

        user = User.fromDict(user_dc)
        return user
