from Database.db_postgres import Postgres_DB
from datetime import datetime
import hashlib
import uuid

class Login:

    def __init__(self) -> None:
        self.db = Postgres_DB("ownerdb", "X$Oi815H%nd*FLyB!9v%", "postgres-data", "5432", "exchange")

    def __checkPassword__(self, hashed_password, user_password) -> None: 
        password, salt = hashed_password.split(':') 
        return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()
    
    def __findLogin__(self, login:str) -> list:
        return self.db.GetUserData(login)

    def send_login(self, login:str, password:str, ip:str) -> dict:
        data = self.__findLogin__(login)
        if data == None:
            return {"resualt" : False}
        resualt = self.__checkPassword__(data[1], password)
        if resualt == True:
            print("user login in {0}, ip {1}".format(login, ip))
        return {"resualt" : resualt}