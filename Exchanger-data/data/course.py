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

    xml_tegs_coins = { "BTC" : "BTC", "USDT" : "USDTERC20", "ETH" : "ETH"}
    xml_tegs_banks = {"Sberbank" : "SBERRUB", "Alfabank" : "ACRUB", "Raiffeisen" : "RFBRUB", "Tinkoff" : "TCSBRUB"}
    xml_tegs_amount = { "BTC" : "2", "USDT" : "50000", "ETH" : "10"}
    
    def __init__(self) -> None:
        self.redis_db = Redis_DB()

    def get_course(self) -> dict:
        return self.__parse_course__(self.redis_db.getValueList("tradepreference"), self.redis_db.getValueMapping("courses"))
    
    def get_course_xml(self) -> dict:
        return self.__parse_course_xml__(self.redis_db.getValueList("tradepreference"), self.redis_db.getValueMapping("courses"))
    
    def __find_course__(self, name:str, course:dict) -> dict:
        pass

    def __parse_course_xml__(self, preference:list, course:dict) -> dict:
        outdata = """<?xml version="1.0"?><rates>"""
        try:
            for data_pref in preference:
                jsdata = json.loads(data_pref)
                coin_name = jsdata['coin']
                coin_name_out = self.xml_tegs_coins.get(coin_name)
                bank_name_out = self.xml_tegs_banks.get(jsdata["name_des"])
                amount = self.xml_tegs_amount.get(coin_name)
                course_out = course.get("{0}:{1}".format(coin_name, jsdata["name_des"]))
                outdata += """<item><from>{0}</from><to>{1}</to><in>{2}</in><out>1</out><amount>{3}</amount><minamount>2000 RUB</minamount><maxamount>1000000 RUB</maxamount>
                            <param>manual</param></item>""".format(bank_name_out, coin_name_out, course_out, amount)
        except Exception as e:
            print("Error send xml course", e, flush=True)
        return outdata + "</rates>"
    
    def __parse_course__(self, preference:list, course:dict) -> dict:
        outdata = {}
        try:
            for data_pref in preference:
                jsdata = json.loads(data_pref)
                coin_name = jsdata['coin']
                bank_name = jsdata["name_des"]
                if outdata.get(coin_name) == None:
                    outdata.update({coin_name : {}})
                coin_data = outdata.get(coin_name)
                course_data = course.get("{0}:{1}".format(coin_name, bank_name))
                coin_data.update({bank_name : course_data})
                outdata.update({coin_name : coin_data})
        except Exception as e:
            print("Error send json course", e, flush=True)
        return outdata