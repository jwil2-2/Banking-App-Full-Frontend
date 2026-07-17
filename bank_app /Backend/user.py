# User domain models, validation, and MongoDB serialization.

import re

class User:
  # Represents an application user and validates registration input.

  def __init__(self, name, email, password, role="user", userId=None):
    self.setName(name)
    self.setEmail(email)
    self.setPassword(password)
    self.__role = role
    self.__userId = userId


  def getName(self):
    return self.__name

  def getEmail(self):
    return self.__email

  def getPassword(self):
    return self.__password

  def getUserId(self):
    return self.__userId
  
  def getRole(self):
    return self.__role

  def setEmail(self, email):
    # Validate and assign a basic email-address format.
    regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

    if re.fullmatch(regex, email):
      self.__email = email
    else:
      raise ValueError("Email needs to be in correct syntax")

  def setName(self, name):
    # Validate a name containing letters, spaces, apostrophes, or hyphens.
    regex = r"^[a-zA-Z]+([ '-][a-zA-Z]+)*$"

    if re.fullmatch(regex, name):
      self.__name = name
    else:
      raise ValueError("Name needs to be in correct syntax")

  def setPassword(self, password):
    # Require 8+ characters with upper, lower, digit, and special.
    regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"

    if re.fullmatch(regex, password):
      self.__password = password
    else:
      raise ValueError(
        "Password must be at least 8 characters and include 1 uppercase letter, 1 lowercase letter, 1 number, and 1 special character."
      )
  
  def setUserId(self, user_id):
    # Assign the ID generated after a MongoDB insert.
    self.__userId = user_id
    
  def toDict(self) -> dict:
    # Serialize fields for persistence, excluding the generated ID.
    # The service replaces the plaintext password with bcrypt before insertion.
    dc = {
      "name": self.__name,
      "email": self.__email,
      "password": self.__password,
      "role": self.__role,
    }
    return dc
  
  @classmethod
  def fromDict(cls, dc:dict) -> "User":
    # Build the proper user subtype from a MongoDB document.
    # Bypass __init__ so stored bcrypt hashes are not validated as plaintext.
    targetCls = AdminUser if dc.get("role") == "admin" else User
    user = targetCls.__new__(targetCls)
    user._User__name = dc["name"]
    user._User__email = dc["email"]
    user._User__password = dc["password"]
    user._User__role = dc.get("role", "user")
    user._User__userId = str(dc["_id"])
    return user


class AdminUser(User):
    # User subtype whose role is always admin.

    def __init__(self, name, email, password):
        super().__init__(name, email, password, role="admin")