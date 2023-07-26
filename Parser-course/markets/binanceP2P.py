from markets.market import MarketP2P
from enum import Enum
from datetime import datetime
import asyncio
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
    
    def __parsData__(self, data, minOrders):
        for lot in data:
            temp = lot['advertiser']
            if self.name != temp['nickName'] and minOrders <= temp['monthOrderCount']:
                temp = lot['adv']
                return temp['price']
        return "0"

    def __findMyPrice__(self, data):
        for lot in data:
            temp = lot['advertiser']
            if self.name == temp['nickName']:
                temp = lot['adv']
                return temp['price']
        return None

    async def __ParseAllData__(self, data:list) -> list:
        rdata = []
        for temp in data:
            parseData = []
            for lot in temp:
                info = {}
                advertiser = lot['advertiser']
                adv = lot['adv']
                info.update({"name" : advertiser['nickName']})
                info.update({"orders" : advertiser['monthOrderCount']})
                info.update({"price" : adv['price']})
                info.update({"finishRate" : advertiser['monthFinishRate']})
                info.update({"surplusAmount" : adv['surplusAmount']})
                info.update({"minSingleTransAmount" : adv['minSingleTransAmount']})
                info.update({"maxSingleTransAmount" : adv['dynamicMaxSingleTransAmount']})
                parseData.append(info)
            rdata += parseData
        return rdata
    
    async def GetAllTickets(self, PaymentMethods: Enum, Fiat: Enum, Lot: Enum, Operation: Enum, maxPages: int, session) -> dict:
        parseData = {}
        data = []
        tasks = []
        for page in range(1, maxPages):
            tasks.append(asyncio.create_task(self.__get_server_data__(Fiat.name, Lot.name, [PaymentMethods.name], Operation.name, 0, page, 20, session)))
        temp = await asyncio.gather(*tasks)
        data = await self.__ParseAllData__(temp)
        parseData.update({'data': data})
        parseData.update({'fiat': Fiat.name})
        parseData.update({'payMethod': PaymentMethods.name})
        parseData.update({'lot': Lot.name})
        return parseData
        #data.append(parseData)

    async def GetBestPrice(self, PaymentMethods: str, Fiat: str, Lot: str, Operation: str, Filter: int, MinOrders: int, session):
        data = await self.__get_server_data__(Fiat, Lot, [PaymentMethods], Operation, Filter, 1, 10, session)
        return self.__parsData__(data, MinOrders)

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