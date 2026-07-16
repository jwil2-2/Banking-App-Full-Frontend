# This class is for creation and storage of a user
import re

class User:

  # Constructor for user initialization
  def __init__(self, name, email, password, role="user", userId = None):
    self.setName(name)
    self.setEmail(email)
    self.setPassword(password)
    self.__role = role


  # Method for encapsulation and returning name
  def getName(self):
    return self.__name

  # Method for encapsulation and returning email
  def getEmail(self):
    return self.__email

  # Method for encapsulation and returning password
  def getPassword(self):
    return self.__password

  # Method for encapsulation and returning userId
  def getUserId(self):
    return self.__userId
  
  # Method for encapsulation and returning userId
  def getRole(self):
    return self.__role

  # Method for encapsulation and setting email with specific rules
  def setEmail(self, email):

    #pattern to include email domain format (email@gmail.com)
    regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

    #comparison for error checking
    if re.fullmatch(regex, email):
      self.__email = email
    else:
      raise ValueError("Email needs to be in correct syntax")

  # Method for encapsulation and setting name 
  def setName(self, name):

    #pattern to include lower and uppercase letters, one hyphen or space, immedietely followed by letters
    #no numbers allowed
    regex = r"^[a-zA-Z]+([ '-][a-zA-Z]+)*$"

    #comparison for error checking
    if re.fullmatch(regex, name):
      self.__name = name
    else:
      raise ValueError("Name needs to be in correct syntax")

  # Method for encapsulation and setting password with 8+ chars, 1 upper, 1 lower, 1 digit, 1 special char
  def setPassword(self, password):

    #pattern for checking password
    regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"

    #comparison for error checking
    if re.fullmatch(regex, password):
      self.__password = password
    else:
      raise ValueError(
        "Password must be at least 8 characters and include 1 uppercase letter, 1 lowercase letter, 1 number, and 1 special character."
      )
  
  def setUserId(self, user_id):
    # called once, after Mongo assigns the real _id on insert
    self.__userId = user_id
    
  #Method for converting object to storable text in mongoDB
  def toDict(self) -> dict:
    dc = {
      "name": self.__name,
      "email": self.__email,
      "password": self.__password,   # already hashed
      "role": self.__role,
    }
    return dc
  
  #Method for returning user object from dict in database
  @classmethod
  def fromDict(cls, dc:dict) -> "User":
    targetCls = AdminUser if dc.get("role") == "admin" else User
    user = targetCls.__new__(targetCls) # bypass __init__, avoids re-validating/re-hashing
    user._User__name = dc["name"]
    user.__User__name = dc["name"]
    user._User__email = dc["email"]
    user._User__password = dc["password"]
    user._User__role = dc.get("role", "user")
    user._User__userId = str(dc["_id"])
    return user


#Subclass of user to give special methods to users who are admins 
# (work in progress)
class AdminUser(User):
    def __init__(self, name, email, password):
        super().__init__(name, email, password, role="admin")






