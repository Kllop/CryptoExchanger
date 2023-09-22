from markets.market import MarketP2P
from datetime import datetime
import json


class ByBit2P2(MarketP2P):
    url = "https://api2.bybit.com/fiat/otc/item/online"
    header = {'User-Agent' : "PostmanRuntime/7.29.0", 'Accept':'*/*', 'Accept-Encoding':'gzip, deflate, br', 'Connection':'keep-alive', 'Content-Type': "application/json"}
    #body = {"page":1,"rows":10,"payTypes":[],"publisherType":None,"asset":"SHIB","tradeType":"BUY","fiat":"RUB", 'transAmount': 100000}

    async def __get_server_data__(self, fiat:str, lot:str, paymethod:list, operation:int, page:int, session):
        try:
            body = {"userId": "", "tokenId": lot, "currencyId": fiat, "payment": paymethod, "side": operation, "size": "10","page": page, "amount": "", "authMaker": False,"canTrade": False}
            body = json.dumps(body)
            if self._isUseProxy:
                header = {'User-Agent' : "PostmanRuntime/7.29.0", 'Accept':'*/*', 'Accept-Encoding':'gzip, deflate, br', 'Connection':'keep-alive', 'Content-Type': "application/json", 
                          "X-Forwarded-For" : self._proxy.GetProxy(), "X-Real-IP" : self._proxy.GetProxy()}
                response = await session.post(self.url, headers = header, data = body, proxy='http://{0}'.format(self._proxy.GetProxy()), timeout = self._ConnectionTimeout)
            else:
                response = await session.post(self.url, headers = self.header, data = body, timeout = self._ConnectionTimeout)
            jdata = await response.text(encoding="UTF-8")
            data = json.loads(jdata)['result']['items']
        except Exception as e:
            print("{0} Error load data bybit".format(datetime.today().strftime('%Y-%m-%d %H:%M:%S')), e, flush=True)
            return {}
        return data
    
    async def __AvgPriceData__(self, data:list) -> list:
        price = []
        if len(data) == 0:
            return 0
        for temp in data:
            price.append(float(temp['price']))
        return round((sum(price) / len(price)), 2) 
    
    async def GetBestPrice(self, PaymentMethods: str, Fiat: str, Lot: str, Operation: int, session):
        data = await self.__get_server_data__(Fiat, Lot, [PaymentMethods], Operation, "1", session)
        return await self.__AvgPriceData__(data)