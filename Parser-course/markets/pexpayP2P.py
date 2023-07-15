from markets.market import MarketP2P
from enum import Enum
from datetime import datetime
import traceback
import requests
import asyncio
import json

class Pexpay2P2(MarketP2P):
    url = 'https://www.pexpay.com/bapi/c2c/v1/friendly/c2c/ad/search'
    header = {'User-Agent': "PostmanRuntime/7.29.0", 'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate, br',
              'Connection': 'keep-alive', 'Content-Type': "application/json"}
    session:requests.Session

    async def __get_data_server__(self, Fiat: str, Lot: str, PayMethod: str, Operation: str, filter: int, page:int, rows:int, session):
        try:
            data = []
            body = await self.__getBody__(Fiat, Lot, PayMethod, Operation, filter, page, rows)
            if self._isUseProxy:
                responce = await session.post(self.url, headers=self.header, json=body,  proxy = 'http://{0}'.format(self._proxy.GetProxy()), timeout = self._ConnectionTimeout)
            else:
                responce = await session.post(self.url, headers=self.header, json=body, timeout = self._ConnectionTimeout)
            jdata = await responce.text(encoding="UTF-8")
            data = json.loads(jdata)['data']
            return data
        except Exception as e:
            print("{0} Error load data pexpay".format(datetime.today().strftime('%Y-%m-%d %H:%M:%S')), e, flush=True)
            return []

    async def __getBody__(self, Fiat:str, Lot:str, PayMethod:str, Operation:str, filter:int, page:int, rows:int):
        body = {"page": page, "rows": rows, "payTypes": [PayMethod], "classifies": [], "asset": Lot, "tradeType": 
                Operation, "fiat": Fiat, "filter": {"payTypes": []}, "transAmount": str(filter)}
        return body

    def __parsData__(self, data, minOrders):
        for lot in data:
            Details = lot['advertiserVo']
            LotInformation = lot['adDetailResp']
            Orders = Details['userStatsRet']
            if self.name != Details['nickName'] and minOrders <= Orders['completedOrderNum']:
                return LotInformation['price']
        return "0"

    def __findMyPrice(self, data):
        for lot in data:
            Details = lot['advertiserVo']
            LotInformation = lot['adDetailResp']
            if self.name == Details['nickName']:
                return LotInformation['price']
        return "0"

    async def __ParseAllData__(self, data:list):
        rdata = []
        for temp in data:
            if temp == None:
                return []
            parseData = []
            for lot in temp:
                info = {}
                Ticket = lot['adDetailResp']
                userInfo = lot['advertiserVo']
                Rait = userInfo['userStatsRet']
                info.update({"name" : userInfo['nickName']})
                info.update({"orders" : Rait['completedOrderNum']})
                info.update({"price" : Ticket['price']})
                info.update({"finishRate" : Rait['finishRate']})
                info.update({"surplusAmount" : Ticket['remainingAmount']})
                info.update({"minSingleTransAmount" : Ticket['minSingleTransAmount']})
                info.update({"maxSingleTransAmount" : Ticket['maxSingleTransAmount']})
                parseData.append(info)
            rdata += parseData
        return rdata

    def GetBestPrice(self, PaymentMethods: Enum, Fiat: Enum, Lot: Enum, Operation: Enum, Filter: int, MinOrders: int):
        data = self.__get_data_server__(Fiat.name, Lot.name, PaymentMethods.name, Operation.name, Filter, 1, 10)
        return self.__parsData__(data, MinOrders)

    def GetMyPrice(self, PaymentMethods: Enum, Fiat: Enum, Lot: Enum, Operation: Enum, Filter: int, maxPages: int):
        if self.name == "":
            return "0"
        data = self.__get_data_server__(Fiat.name, Lot.name, PaymentMethods.name, Operation.name, Filter, 1, 10)
        return self.__findMyPrice(data)
    
    async def GetAllTickets(self, PaymentMethods: Enum, Fiat: Enum, Lot: Enum, Operation: Enum, maxPages: int, session) -> list:
        parseData = {}
        data = []
        tasks = []
        temp = []
        for page in range(1, maxPages):
            #temp.append(await self.__get_data_server__(Fiat.name, Lot.name, PaymentMethods.name, Operation.name, 0, page, 20, session))
            tasks.append(asyncio.create_task(self.__get_data_server__(Fiat.name, Lot.name, PaymentMethods.name, Operation.name, 0, page, 20, session)))
            #await asyncio.sleep(1)
        temp = await asyncio.gather(*tasks)
        data = await self.__ParseAllData__(temp)
        parseData.update({'data': data})
        parseData.update({'fiat': Fiat.name})
        parseData.update({'payMethod': PaymentMethods.name})
        parseData.update({'lot': Lot.name})
        return parseData
        
