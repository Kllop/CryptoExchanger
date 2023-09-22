from Database import Postgres_DB
from Database import Redis_DB
import json

class DirectionPreference:

       redis_db = Redis_DB()
       postgres_db = Postgres_DB("ownerdb", "X$Oi815H%nd*FLyB!9v%", "postgres-data", "5432", "exchange")

       def createDirection(self):
              
              self.postgres_db.ClearTable("DirectionPreference")
              
              self.postgres_db.SendDirectoion("1", "BTC",  "64", "Райффайзен RUB", "Raiffeisen RUB", "Raiffeisen", 5.00, "P2P", "Bybit")
              self.postgres_db.SendDirectoion("2", "ETH",  "64", "Райффайзен RUB", "Raiffeisen RUB", "Raiffeisen", 5.00, "P2P", "Bybit")
              self.postgres_db.SendDirectoion("3", "USDT", "64", "Райффайзен RUB", "Raiffeisen RUB", "Raiffeisen", 5.00, "P2P", "Bybit")

              self.postgres_db.SendDirectoion("4", "BTC",  "582", "Сбербанк RUB", "Sberbank RUB", "Sberbank", 5.00, "P2P", "Bybit")
              self.postgres_db.SendDirectoion("5", "ETH",  "582", "Сбербанк RUB", "Sberbank RUB", "Sberbank", 5.00, "P2P", "Bybit")
              self.postgres_db.SendDirectoion("6", "USDT", "582", "Сбербанк RUB", "Sberbank RUB", "Sberbank", 5.00, "P2P", "Bybit")

              self.postgres_db.SendDirectoion("7", "BTC",  "581", "Тинькофф RUB", "Tinkoff RUB", "Tinkoff", 5.00, "P2P", "Bybit")
              self.postgres_db.SendDirectoion("8", "ETH",  "581", "Тинькофф RUB", "Tinkoff RUB", "Tinkoff", 5.00, "P2P", "Bybit")
              self.postgres_db.SendDirectoion("9", "USDT", "581", "Тинькофф RUB", "Tinkoff RUB", "Tinkoff", 5.00, "P2P", "Bybit")

       def setReidsDirection(self):
              postgre_data = self.postgres_db.GetDirection()
              self.redis_db.removeKey("tradepreference")
              for data in postgre_data:
                     send_data = {"uid" : data[0], "coin" : data[1], "name_exch" : data[2], "name_ru" : data[3], "name_en" : data[4], "name_des" : data[5], "percent" : data[6], "area" : data[7], "market" : data[8]}
                     self.redis_db.setValueList("tradepreference", json.dumps(send_data))