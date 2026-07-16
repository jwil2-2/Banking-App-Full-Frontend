import asyncio
import os

from .transaction import Transaction
from .user import User, AdminUser
from decimal import Decimal
from .Services.accountService import AccountService
from fastapi import FastAPI
from .Repositories.accountRepository import AccountRepository
from .Repositories.userRepository import UserRepository
from .Repositories.transactionRepository import TransactionRepository
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

# shared service instances, used by both the console app and (eventually) more controllers
_accountRepository = AccountRepository()
_userRepository = UserRepository()
_transactionRepository = TransactionRepository()
accService = AccountService(_accountRepository, _transactionRepository)


#class for bank business logic for transactions
class Bank:

    
    def deposit(user, account, money) :
        #checks for depositing negative values and raising errors
        if money < 0 :
            raise ValueError("Money deposited must be positve")
        
        from accounts import Account

        account.setBalance(money)

    
    def withdraw(user, account, money) :
        
        from accounts import Account
        #check for not withdrawing more money than in the current account
        if money < 0 :
            raise ValueError("Money to be withdrawn needs to be positive")
        elif account.getBalance() < money :
            raise ValueError("Not enough money in account")
        
        #set to negative to remove from account
        account.setBalance(-money)


#Helper method to fromat output in money format
def formatMoney(amount):
    return f"${amount:,.2f}"
        
        
# Starting point for application
# Handles user prompting and calls to associated classes 
# and methods needed for bank application

async def main() -> None:

    #True variable for infinite loop unless exited, or error
    running = True

    #Initial user profile and account to be made and used by user in bank app session
    user = None
    account = None

    #While loop to keep program running for as long as the user wants with 
    #Unless and error is returned or they choose to exit the program
    while running :
        print("\nWelcome to the Bank!")
        print("1: Create Profile")
        print("2: Create Checking Account")
        print("3: Create Savings Account")
        print("4: View Transaction History")
        print("5: View Account Details")
        print("6: Deposit")
        print("7: Withdraw")
        print("8: Exit\n")


        str = input("Enter selection: ")
        print("\n")
        
        # if else cases for each user selection
        if str == '1':
            #getting user information and checking to create admin account
            name = input("Enter name: ")
            email = input("Enter email: ")
            password = input("Enter password: ")
            is_admin = input("Is this an admin? (y/n): ").lower()
            print("\n")
            if is_admin == "y":
                user = AdminUser(name, email, password)
            else:
                user = User(name, email, password)
            
            # persist the new user and capture the real Mongo id
            userId = await _userRepository.create(user.toDict())
            user.setUserId(userId)

            print("Profile created!")
        
        elif str == '2':
            #error checking for current session have user created
            if user == None :
                raise ReferenceError("No profile found")
            #creating and using checking account, also check if user profile made
            account = await accService.createAccount(user, "Checking")
            print("Account created and in use!")
        
        elif str == '3':
            #error checking for current session have user created
            if user == None :
                raise ReferenceError("No profile found")
            #creating and using savings account, also check if user profile made
            account = await accService.createAccount(user.getUserId(), "Savings")
            print("Account created and in use!")
        
        elif str == '4':
            if user == None :
                raise ReferenceError("No profile found")
            if account == None :
                raise ReferenceError("No account created")
            #getting transactions from current account, also making sure user profile is made
            #(need to implement) transactions = await _transactionRepository.get_by_account(account.getAccountId())
            transactions: Transaction = account.getTransactions()

            print("Transactions from current account: \n")
            #print out each transaction from the list associated with account
            for item in transactions:
                print(item.getTranType(), item.getAmount())

            print("Account Balance:", formatMoney(account.getBalance()))
        
        elif str == '5':
            #error checking for current session have user and bank account created
            if user == None :
                raise ReferenceError("No profile found")
            if account == None :
                raise ReferenceError("No account created")
            
            #retrieving account details from account method to be printed back to user
            details = account.getAccountDetails()
            print("Account Details:")
            print("Account ID:", details["Account ID"])
            print("Account Type:", details["Account Type"])
            print("User ID:", details["User ID"])
            print("Balance:", formatMoney(details["Balance"]))
        elif str == '6':
            #error checking for current session have user and bank account created
            if user == None :
                raise ReferenceError("No profile found")
            if account == None :
                raise ReferenceError("No account created")
            #Getting deposit amount from user and calling bank service method for logic and addition to account
            money = Decimal(input("Enter amount: $"))
            Bank.deposit(user, account, money)

            #Add transaction history to current account
            account.addTransaction(Transaction("Deposit", money))
            print("Deposit successful!\n")
        
        elif str == '7':
            #error checking for current session have user and bank account created
            if user == None :
                raise ReferenceError("No profile found")
            if account == None :
                raise ReferenceError("No account created")
            
            #Getting withdrawal amount from user and calling bank service for logic and subtraction from account
            money = Decimal(input("Enter amount: $"))
            Bank.withdraw(user, account, money)

            #Add transaction history to current account
            account.addTransaction(Transaction("Withdrawal", money))
            print("Withdrawal successful!\n")

        elif str == '8':
            #False variable would now close loop and exit program
            running = False
        else :
            #If user provides another input not on menu it leads to this error
            raise KeyError("Invalid selection")




if __name__ == "__main__":
    asyncio.run(main())