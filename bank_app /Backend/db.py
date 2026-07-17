# Configures the asynchronous MongoDB client and application collections.
# All repositories share the bank_app database configured through MONGO_URI.

import os

from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()

mongo_uri = os.getenv("MONGO_URI")  

client = AsyncIOMotorClient(mongo_uri)
db = client["bank_app"]

users_collection = db["users"]
accounts_collection = db["accounts"]
transactions_collection = db["transactions"]