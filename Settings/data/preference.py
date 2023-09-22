from Database import Postgres_DB
from Database import Redis_DB
import json
import uuid

class DirectionPreference:

       redis_db = Redis_DB()
       postgres_db = Postgres_DB("ownerdb", "X$Oi815H%nd*FLyB!9v%", "postgres-data", "5432", "exchange")
       postgres_db.DropTable("DirectionPreference")

       def createDirection(self, coin:str, pay_method:str, bank_ru:str, bank_en:str, bank_ind:str, percent:str, area:str, market:str):       
              self.postgres_db.SendDirectoion(uuid.uuid4().hex, coin, pay_method, bank_ru, bank_en, bank_ind, percent, area, market)

       def getAllDirection(self):
              return self.postgres_db.GetAllDirection()
       
       def removeDirection(self, uid:str):
              self.postgres_db.RemoveDirection(uid)

       def setReidsDirection(self):
              postgre_data = self.postgres_db.GetDirection()
              self.redis_db.removeKey("tradepreference")
              for data in postgre_data:
                     send_data = {"uid" : data[0], "coin" : data[1], "name_exch" : data[2], "name_ru" : data[3], "name_en" : data[4], "name_des" : data[5], "percent" : data[6], "area" : data[7], "market" : data[8]}
                     self.redis_db.setValueList("tradepreference", json.dumps(send_data))