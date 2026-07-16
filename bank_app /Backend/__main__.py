import os

from fastapi import FastAPI
from .Controllers.accountController import router as account_router
from .Controllers.userController import router as user_router

from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

#instance of app
app = FastAPI()
app.include_router(account_router)
app.include_router(user_router)

frontend_origins = [origin.strip() for origin in os.getenv("FRONTEND_ORIGINS", "").split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=frontend_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)