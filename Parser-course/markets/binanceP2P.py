from markets.market import MarketP2P
from datetime import datetime
import json


class Binance2P2(MarketP2P):
    url = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"
    header = {'User-Agent' : "PostmanRuntime/7.29.0", 'Accept':'*/*', 'Accept-Encoding':'gzip, deflate, br', 'Connection':'keep-alive', 'Content-Type': "application/json"}
    #body = {"page":1,"rows":10,"payTypes":[],"publisherType":None,"asset":"SHIB","tradeType":"BUY","fiat":"RUB", 'transAmount': 100000}

    async def __fill_body__(self, body:dict , fiat:str, lot:str, paymethod:str, operation:str, filter:int, page:int, rows:int):
        body.update()
        body.update({})
        body.update({})
        body.update({})
        body.update({})
        body.update({})
        if(filter != 0):
            body.update({})

    async def __get_server_data__(self, fiat:str, lot:str, paymethod:str, operation:str, filter:int, page:int, rows:int, session):
        try:
            body = {"page":1,"rows":20,"payTypes":[],"publisherType":None,"asset":"SHIB","tradeType":"BUY","fiat":"RUB"}        
            body.update({'fiat': fiat, 'rows': rows, 'tradeType': operation, 'asset': lot, 'payTypes': paymethod, 'page': page, 'transAmount': filter})
            body = json.dumps(body)
            if self._isUseProxy:
                response = await session.post(self.url, headers = self.header, data = body, proxy='http://{0}'.format(self._proxy.GetProxy()), timeout = self._ConnectionTimeout)
            else:
                response = await session.post(self.url, headers = self.header, data = body, timeout = self._ConnectionTimeout)
            jdata = await response.text(encoding="UTF-8")
            data = json.loads(jdata)['data']
        except Exception as e:
            print("{0} Error load data binance".format(datetime.today().strftime('%Y-%m-%d %H:%M:%S')), e, flush=True)
            return {}
        return data

    async def __AvgPriceData__(self, data:list) -> list:
        price = []
        if len(data) == 0:
            return 0
        for temp in data:
            adv = temp['adv']
            price.append(float(adv['price']))
        return round((sum(price) / len(price)) * 1.05, 2) 
    

    async def GetBestPrice(self, PaymentMethods: str, Fiat: str, Lot: str, Operation: str, Filter: int, MinOrders: int, session):
        data = await self.__get_server_data__(Fiat, Lot, [PaymentMethods], Operation, Filter, 1, 10, session)
        parseData = {}
        price = await self.__AvgPriceData__(data)
        if price == 0:
            return {}
        parseData.update({'AVGprice': price})
        parseData.update({'fiat': Fiat})
        parseData.update({'payMethod': PaymentMethods})
        parseData.update({'lot': Lot})
        return parseData

    def GetMyPrice(self, PaymentMethods: str, Fiat: str, Lot: str, Operation: str, Filter: int, maxPages: int):
        if self.name == '':
            return "0"
        for page in range(1, maxPages):
            data = self.__get_server_data__(Fiat.name, Lot.name, [PaymentMethods], Operation.name, Filter, page, 20)
            if len(data) == 0:
                return "0"
            price = self.__findMyPrice__(data)
            if price != None:
                return price
        return "0"