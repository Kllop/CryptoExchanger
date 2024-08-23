from Database import Postgres_DB

class UsersInfo:
    
    def __init__(self) -> None:
        self.postgres_db = Postgres_DB("ownerdb", "X$Oi815H%nd*FLyB!9v%", "postgres-data", "5432", "exchange")

    def GetAllUsers(self):
        return self.postgres_db.getAllUsers()

    def GetUserDetail(self, user_id:int):
        return self.postgres_db.GetUserDetail(user_id)