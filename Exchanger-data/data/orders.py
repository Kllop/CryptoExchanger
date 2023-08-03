from Database.db_postgres import Postgres_DB
from datetime import datetime

class Orders:

    def __init__(self) -> None:
        self.db = Postgres_DB("ownerdb", "X$Oi815H%nd*FLyB!9v%", "postgres-data", "5432", "exchange")

    def decryptOrderID(self, order_id) -> None:
        return "Hello"

    def send_order(self, request_data:dict) -> dict:
        order_id = self.__generateOrderId__()
        date_create = self.__dateTimeNow__()
        date_change = self.__dateTimeNow__()
        course = "127000.20"    
        coin = request_data['getterType']
        price = float(request_data['setterValue'])
        count = 1.00
        telegram = request_data['setterTelegram']
        pay_method = request_data['setterType']
        pay_method_number = request_data['setterNumber']
        wallet = request_data['getterNumber']
        status = "new order"
        self.db.SendOrder(order_id, date_create, date_change, course, coin, price, count, telegram, pay_method, pay_method_number, wallet, status)
        return {"resualt" : True, "OrderID" : order_id, "data" : {}}

    def __generateOrderId__(self) -> int:
        return self.db.GetLastOrderID() + 1
    
    def __dateTimeNow__(self) -> str:
        return datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    def RemoveTable(self) -> None:
        self.db.DropTable("OrdersList")