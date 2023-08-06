from Database.db_postgres import Postgres_DB
from datetime import datetime
from data.course import Course
from cryptography.fernet import Fernet

class Orders:
    secret_key = b'p3guEPuaLDyekB7fIec45Bc_ajqWZFnpfTqBzUjML3c='

    def __init__(self) -> None:
        self.db = Postgres_DB("ownerdb", "X$Oi815H%nd*FLyB!9v%", "postgres-data", "5432", "exchange")
        key = Fernet.generate_key()
        print(key, flush=True)
        self.fl = Fernet(key)

    def decryptOrderID(self, order_id) -> str:
        return str(hash(order_id))#self.fl.decrypt(str(order_id))
    
    def encryptOrderID(self, order_id) -> int:
        return hash(order_id)#self.fl.encrypt(str(order_id).encode())

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
        out_order_id = self.encryptOrderID(order_id)
        print(out_order_id, flush=True)
        return {"resualt" : True, "OrderID" : out_order_id, "data" : {"price" : price, "bank_name" : "Tinkoff RUB", "bank_number" : "1232132312", "bank_owner_name" : "Алексей К.", "setter_number" : pay_method_number, "pay_type" : pay_method, "count" : count, "wallet" : wallet, "coin" : coin}}

    def __generateOrderId__(self) -> int:
        data = self.db.GetLastOrderID()
        if data == None:
            return 1
        return data + 1
    
    def __dateTimeNow__(self) -> str:
        return datetime.now().strftime("%d.%m.%Y %H:%M")
    
    def RemoveTable(self) -> None:
        self.db.DropTable("OrdersList")