from Database.db_postgres import Postgres_DB
from datetime import datetime
from data.course import Course

class Orders:

    def __init__(self) -> None:
        self.db = Postgres_DB("ownerdb", "X$Oi815H%nd*FLyB!9v%", "postgres-data", "5432", "exchange")

    def __oderPriceInfo__(self, coin:str, payMethod:str, price:float):
        data = Course().get_course()
        course = data.get(coin).get(payMethod)
        return course, round(price/course, 8)

    def send_order(self, request_data:dict) -> dict:
        order_id = self.__generateOrderId__()
        date_create = self.__dateTimeNow__()
        date_change = self.__dateTimeNow__()
        price = float(request_data['setterValue'])
        coin = request_data['getterType']
        pay_method = request_data['setterType']
        course, count = self.__oderPriceInfo__(coin, pay_method, price)    
        telegram = request_data['setterTelegram']
        pay_method_number = request_data['setterNumber']
        wallet = request_data['getterNumber']
        status = "new order"
        self.db.SendOrder(order_id, date_create, date_change, course, coin, price, count, telegram, pay_method, pay_method_number, wallet, status)
        return {"resualt" : True, "OrderID" : order_id}

    def __generateOrderId__(self) -> int:
        data = self.db.GetLastOrderID()
        if data == None:
            return 1
        return data + 1
    
    def getOrder(self, order_id:str) -> dict:
        data = self.db.getOrderWithOrderID(order_id)
        if len(data) == 0:
            return {"resualt" : False, "data" : {}}
        return {"resualt" : True, "data" : {"orderID" : order_id, "price" : data[5], "bank_number" : "2200700834422205", 
                                            "bank_owner_name" : "Ксения А.", "setter_number" : data[9], "pay_type" : "Tinkoff RUB", 
                                            "count" : data[6], "wallet" : data[10], "coin" : data[4], "status" : data[11], "change_time" : data[2]}}

    def __dateTimeNow__(self) -> str:
        return datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    def RemoveTable(self) -> None:
        self.db.DropTable("OrdersList")