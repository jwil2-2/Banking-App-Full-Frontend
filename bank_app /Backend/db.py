from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

# Load the variables from the .env file
load_dotenv()

#get url from .env file
mongo_uri = os.getenv("MONGO_URI")  

client = AsyncIOMotorClient(mongo_uri)
db = client["bank_app"]

#tables in mongoDB to be filled in
users_collection = db["users"]
accounts_collection = db["accounts"]
transactions_collection = db["transactions"]