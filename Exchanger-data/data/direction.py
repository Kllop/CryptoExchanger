from Database.db_redis import Redis_DB
import json

class direction:
#"ETH" : [{"key" : "Sberbank", "name" : "Сбербанк RUB"}, 
#         {"key" : "Alfabank", "name" : "Альфабанк RUB"}, 
#         {"key" :"Uralsib", "name" : "Уралсиб RUB"}]
 
     
    def __init__(self) -> None:
        self.redis_db = Redis_DB()

    def __parsing__(self, data) -> dict:
        pass

    def get_direction(self) -> dict:
        preference = self.parse_preference(self.redis_db.getValueList("tradepreference"))

    def parse_preference(data:dict) -> dict:
        outdata = []
        for temp in data:
            outdata.append(json.loads(temp))
        return outdata