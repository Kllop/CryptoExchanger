from Database.db_postgres import Postgres_DB
from datetime import datetime
import hashlib
import uuid
import random

class Registraton:

    def __init__(self) -> None:
        self.db = Postgres_DB("ownerdb", "X$Oi815H%nd*FLyB!9v%", "postgres-data", "5432", "exchange")

    def __dateTimeNow__(self) -> str:
        return datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    def send_registraton_user(self, login:str, password:str, email:str, ip:str, referal:str) -> dict:
        return self.__sendRegistraton__(login, password, email, ip, referal, "USER")
    
    def send_registraton_admin(self, login:str, password:str, email:str, ip:str, referal:str) -> dict:
        return self.__sendRegistraton__(login, password, email, ip, referal, "ADMIN")
    
    def __sendRegistraton__(self, in_login:str, in_password:str, email:str, ip:str, referal:str, permision:str) -> dict:
        check = self.__checkFreeSlot__(in_login, email)
        if check.get('resualt') == True:   
            password = self.__hashPassword__(in_password)
            referalcode = self.__hashPassword__(in_login)
            code_id = self.__hashId__(in_password, in_login)
            date = self.__dateTimeNow__()
            self.db.createUser(in_login, password, email, date, date, ip, referal, referalcode, permision, '0', 0, code_id)
            return {"resualt" : True, "message": "", "id" : code_id}
        return {"resualt" : False, "message" : check.get("message"), "id" : ""}

    def __checkFreeSlot__(self, login:str, email:str) -> dict:
        data = self.db.GetFreeUserData(login, email)
        for temp in data:
            if temp[0] == login:
                return {"resualt" : False, "message" : "Login is already taken"}
            elif temp[2] == email:
                return {"resualt" : False, "message" : "Email is already taken"}
        return {'resualt' : True, "message" : ""}
    
    def __hashPassword__(self, password):
        salt = uuid.uuid4().hex 
        return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt
    
    def __hashId__(self, password:str, login:str) -> str:
        salt = uuid.uuid4().hex
        code = self.__randomWords__(password, login)
        return hashlib.sha256(salt.encode() + code.encode()).hexdigest() + ':' + salt
    
    def __randomWords__(self, password:str, login:str) -> str:
        text = password + login
        words = text.split()
        for i, word in enumerate(map(list, words)):
            random.shuffle(word)
            words[i] = ''.join(word)
        return words[0]