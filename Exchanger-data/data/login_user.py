from Database.db_postgres import Postgres_DB
from datetime import datetime
import hashlib

class Login:

    def __init__(self) -> None:
        self.db = Postgres_DB("ownerdb", "X$Oi815H%nd*FLyB!9v%", "postgres-data", "5432", "exchange")

    def __checkPassword__(self, hashed_password, user_password) -> None: 
        password, salt = hashed_password.split(':') 
        return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()
    
    def referal_code(self, code_id:str) -> str:
        url = "https://jango-exchange.com/"
        referal = self.db.GetReferalCodeUserData(code_id)
        if referal == "":
            return {"resualt" : False, "referal" : ""}
        return {"resualt" : True, "referal" : url + "?ref=" + referal}
    
    def referal_count(self, code_id:str) -> str:
        referal = self.db.GetReferalCodeUserData(code_id)
        if referal == "":
            return {"resualt" : False, "count" : 0}
        count = self.db.GetCountReferalUsers(referal)
        return {"resualt" : True, "count" : count}
    
    def referal_bid(self, code_id:str) -> str:
        referal = self.db.GetReferalCodeUserData(code_id)
        referal_bid = self.db.GetReferalBid(referal)
        outdata = []
        for bid in referal_bid:
            outdata.append({'coin' : bid[4], 'summ' : bid[5], 'ref_summ' : bid[5] * 0.005})
        return {"resualt" : bool(len(outdata)), "data" : outdata}
    
    def __findLogin__(self, login:str) -> list:
        return self.db.GetUserData(login)

    def send_login(self, login:str, password:str, ip:str) -> dict:
        data = self.__findLogin__(login)
        if data == None or len(data) == 0:
            return {"resualt" : False, "id" : ""}
        resualt = self.__checkPassword__(data[1], password)
        code_id = data[11]
        if resualt == True:
            print("user login in {0}, ip {1}".format(login, ip))
            return {"resualt" : resualt, "id" : code_id}
        return {"resualt" : False, "id" : ""}
    
    def get_all_users(self) -> list:
        data = self.db.getAllUsers()
        return data