from Database.db_redis import Redis_DB
import json

class Direction:
# OUT
#"ETH" : [{"key" : "Sberbank", "name" : "Сбербанк RUB"}, 
#         {"key" : "Alfabank", "name" : "Альфабанк RUB"}, 
#         {"key" :"Uralsib", "name" : "Уралсиб RUB"}]
 
     
    def __init__(self) -> None:
        self.redis_db = Redis_DB()

    def get_direction(self) -> dict:
        data =  self.__parse_preference__(self.redis_db.getValueList("tradepreference"))
        return data

    def __parse_preference__(self, data:list) -> dict:
        outdata = {}
        for temp in data:      
            data_dir = json.loads(temp)
            coin_name = data_dir['coin']
            if outdata.get(coin_name) == None:
                outdata.update({coin_name : {}})
            temp_data = outdata.get(coin_name)
            temp_data.update({data_dir.get("name_des") : data_dir.get("name_ru")})
        return outdata