import hashlib
import uuid

class Registraton:

    def __init__(self) -> None:
        pass 

    def reg(self, login:str, password:str, email:str, referal:str) -> bool:
        password = self.hash_password(password)

    def hash_password(self, password):
        salt = uuid.uuid4().hex 
        return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt

    def check_password(self, hashed_password, user_password): 
        password, salt = hashed_password.split(':') 
        return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()

