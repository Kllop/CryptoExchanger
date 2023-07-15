from markets.market import MarketP2P
from enum import Enum
from datetime import datetime
import json
import asyncio

class HuobiP2P(MarketP2P):
    url = 'https://otc-akm.huobi.com/v1/data/trade-market?coinId={0}&currency={1}&tradeType={2}&currPage={5}&payMethod={3}&acceptOrder=0&country=&blockType=general&online=1&range=0&amount={4}&onlyTradable=false&isFollowed=false'
    header = {'User-Agent' : "PostmanRuntime/7.29.0", 'Accept':'*/*', 'Accept-Encoding':'gzip, deflate, br', 'Connection':'keep-alive'}
    
    async def __get_server_data__(self, fiat:str, lot:str, paymethod:str, operation:str, filter:int, page:int, session):
        try:
            if self._isUseProxy:
                responce = await session.get(self.url.format(lot, fiat, operation, paymethod, str(filter), page), headers = self.header, proxy = 'http://{0}'.format(self._proxy.GetProxy()), timeout = self._ConnectionTimeout)
            else:
                responce = await session.get(self.url.format(lot, fiat, operation, paymethod, str(filter), page), headers = self.header, timeout = self._ConnectionTimeout)
            jdata = await responce.text(encoding="UTF-8")
            data = json.loads(jdata)['data']
            return data
        except Exception as e:
            print("{0} Error load data huobi".format(datetime.today().strftime('%Y-%m-%d %H:%M:%S')), e, flush=True)
            return {}

    def __parsData__(self, data, minOrders:int):
        for lot in data:
            if self.name != lot['userName'] and minOrders <= lot['tradeMonthTimes']:
                return lot['price']
        return "0"

    def __findMyPrice(self, data):
        for lot in data:
            if self.name == lot['userName']:
                return lot['price']
        return None
    
    async def __pars_payMethods__(self, payMethods):
        return str(payMethods.value)

    async def __ParseAllData__(self, data:list):
        rdata = []
        for temp in data:
            parseData = []
            for lot in temp:
                if lot['isOnline'] == False:
                    continue
                info = {}
                info.update({"name" : lot['userName']})
                info.update({"orders" : lot['tradeMonthTimes']})
                info.update({"price" : lot['price']})
                info.update({"finishRate" : lot['orderCompleteRate']})
                info.update({"surplusAmount" : lot['tradeCount']})
                info.update({"minSingleTransAmount" : lot['minTradeLimit']})
                info.update({"maxSingleTransAmount" : lot['maxTradeLimit']})
                parseData.append(info)
            rdata += parseData
        return rdata
    
    async def __ParsOperation__(self, operation:Enum):
        if operation.name == "SELL":
            return "buy"
        else:
            return "sell"

    def GetBestPrice(self, PaymentMethods: Enum, Fiat: Enum, Lot: Enum, Operation: Enum, Filter: int, MinOrders: int):
        Paymethod = self.__pars_payMethods__(PaymentMethods)
        operation = self.__ParsOperation__(Operation)
        data = self.__get_server_data__(str(Fiat.value), str(Lot.value), Paymethod, operation, Filter, 1)
        return self.__parsData__(data, MinOrders)

    def GetMyPrice(self, PaymentMethods: Enum, Fiat: Enum, Lot: Enum, Operation: Enum, Filter: int, maxPages: int):
        if self.name == '':
            return "0"
        Paymethod = self.__pars_payMethods__(PaymentMethods)
        operation = self.__ParsOperation__(Operation)
        for page in range(1, maxPages):
            data = self.__get_server_data__(str(Fiat.value), str(Lot.value), Paymethod, operation, Filter, page)
            if data == None:
                return "0"
            price = self.__findMyPrice(data)
            if price != None:
                return price
        return "0"
    
    async def GetAllTickets(self, PaymentMethods: Enum, Fiat: Enum, Lot: Enum, Operation: Enum, maxPages: int, session) -> list:
        Paymethod = await self.__pars_payMethods__(PaymentMethods)
        parseData = {}
        data = []
        operation = await self.__ParsOperation__(Operation)
        tasks = []
        for page in range(1, maxPages):
            tasks.append(asyncio.create_task(self.__get_server_data__(str(Fiat.value), str(Lot.value), Paymethod, operation, 0, page, session)))
        temp = await asyncio.gather(*tasks)
        data = await self.__ParseAllData__(temp)
        parseData.update({'data': data})
        parseData.update({'fiat': Fiat.name})
        parseData.update({'payMethod': PaymentMethods.name})
        parseData.update({'lot': Lot.name})
        return parseData