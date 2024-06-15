from Database import Postgres_DB

class OrderInfo:
    
    def __init__(self) -> None:
        self.postgres_db = Postgres_DB("ownerdb", "X$Oi815H%nd*FLyB!9v%", "postgres-data", "5432", "exchange")

    def GetAllOrders(self, status:str):
        return self.postgres_db.GetAllOrders(status)

    def GetOrderDetail(self, order_id:int):
        return self.postgres_db.GetOrderDetail(order_id)