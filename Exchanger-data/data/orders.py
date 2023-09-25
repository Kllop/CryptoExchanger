from Database.db_postgres import Postgres_DB
from Database.db_redis import Redis_DB
from datetime import datetime
from data.course import Course
import json

class Orders:

    def __init__(self) -> None:
        self.db = Postgres_DB("ownerdb", "X$Oi815H%nd*FLyB!9v%", "postgres-data", "5432", "exchange")
        self.redis_db = Redis_DB()

    def __oderPriceInfo__(self, coin:str, payMethod:str, price:float):
        data = Course().get_course()
        course = data.get(coin).get(payMethod)
        print(round(float(price)/float(course), 8), flush=True)
        return course, round(float(price)/float(course), 8)

    def send_order(self, request_data:dict) -> dict:
        order_id = self.__generateOrderId__()
        date_create = self.__dateTimeNow__()
        date_change = self.__dateTimeNow__()
        price = float(request_data['setterValue'])
        coin = request_data['getterType']
        pay_method = request_data['setterType']
        course, count = self.__oderPriceInfo__(coin, pay_method, price)    
        telegram = request_data['setterTelegram']
        email = request_data['setter_email']
        pay_method_number = request_data['setterNumber']
        wallet = request_data['getterNumber']
        status = "new order"
        referal = request_data['referal']
        owner = request_data['owner']
        if owner != "":
            referal = self.db.GetReferalUserData(owner)
        self.db.SendOrder(order_id, date_create, date_change, course, coin, price, count, telegram, pay_method, pay_method_number, wallet, status, referal, owner)
        return {"resualt" : True, "OrderID" : order_id}, course, count

    def __generateOrderId__(self) -> int:
        data = self.db.GetLastOrderID()
        if data == None:
            return 1
        return data + 1
    
    def __getPayMethod__(self, Pay_name:str):
        outdata = self.redis_db.getValueMappingCurrent(Pay_name, "directionbanks")
        if outdata == None:
            return {}
        return json.loads(outdata)
    
    def getAllMyBids(self, code_id:str) -> list:
        data = self.db.GetAll_My_Bids(code_id)
        outdata = []
        for temp in data:
            outdata.append({'coin' : temp[4], 'course' : temp[3], 'summ' : temp[5], 'count' : temp[6], 'status' : temp[11]})
        return outdata
    
    def getOrder(self, order_id:str) -> dict:
        data = self.db.getOrderWithOrderID(order_id)
        pay_data = self.__getPayMethod__(data[8])
        if len(data) == 0:
            return {"resualt" : False, "data" : {}}
        return {"resualt" : True, "data" : {"orderID" : order_id, "price" : data[5], "bank_number" : pay_data.get("bank_number"), "bank_owner_name" : 
                                            pay_data.get("bank_owner"), "setter_number" : data[9], "pay_type" : pay_data.get("bank_ru"), "count" : data[6], 
                                            "wallet" : data[10], "coin" : data[4], "status" : data[11], "change_time" : data[2], "course" : data[3], "telegram" : data[7] }}

    def change_status_order(self, order_id:int, new_status:str) -> dict:
        return self.db.ChangeStatusOrder(order_id, new_status)

    def __dateTimeNow__(self) -> str:
        return datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    def RemoveTable(self) -> None:
        self.db.DropTable("OrdersList")