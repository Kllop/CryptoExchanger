from Database.db_postgres import Postgres_DB
from datetime import datetime
import hashlib
import uuid

class Registraton:

    def __init__(self) -> None:
        self.db = Postgres_DB("ownerdb", "X$Oi815H%nd*FLyB!9v%", "postgres-data", "5432", "exchange")

    def __dateTimeNow__(self) -> str:
        return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    def send_registraton(self, login:str, password:str, email:str, ip:str, referal:str) -> bool:
        password = self.__hashPassword__(password)
        date = self.__dateTimeNow__()
        self.db.createUser(login, password, email, date, date, ip, referal, 0)

    def __hashPassword__(self, password):
        salt = uuid.uuid4().hex 
        return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt