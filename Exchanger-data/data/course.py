from Database.db_redis import Redis_DB
import json

#OUT
#json_export_course = {"BTC" : {"Sberbank" : "2950000", "Alfabank" : "3000000", "Tinkoff" : "2900000"}, 
#                      "ETH" : {"Sberbank" : "185000", "Alfabank" : "187000", "Uralsib" : "186500"}}


#IN course
#{'USDT': '{"AVGprice": 93.01, "fiat": "RUB", "payMethod": "TinkoffNew", "lot": "USDT"}', 
# 'BTC': '{"AVGprice": 2723277.21, "fiat": "RUB", "payMethod": "TinkoffNew", "lot": "BTC"}', 
# 'ETH': '{"AVGprice": 175969.69, "fiat": "RUB", "payMethod": "TinkoffNew", "lot": "ETH"}'}
#
#IN direction
#[{"coin" : data[0], "name_exch" : data[1], "name_ru" : data[2], "name_en" : data[3], "name_des" : data[4], "percent" : data [5], "market" : data[6]}]
class Course:
    
    def __init__(self) -> None:
        self.redis_db = Redis_DB()

    def get_course(self) -> dict:
        return self.__parse_course__(self.redis_db.getValueList("tradepreference"), self.redis_db.getValueMapping("binancecourse"))
    
    def __find_course__(self, name:str, course:dict) -> dict:
        pass

    def __parse_course__(self, preference:list, course:dict) -> dict:
        outdata = {}
        for data_pref in preference:
            jsdata = json.loads(data_pref)
            coin_name = jsdata['coin']
            if outdata.get(coin_name) == None:
                outdata.update({coin_name : {}})
            coin_data = outdata.get(coin_name)
            course_data = json.loads(course.get(coin_name))
            coin_data.update({jsdata["name_des"] : course_data["AVGprice"]})
            outdata.update({coin_name : coin_data})
        return outdata