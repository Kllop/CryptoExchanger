from markets.variebles.EPayMethods import EPaymentMethodsOkexRUB
from markets.market import MarketP2P
from enum import Enum
from datetime import datetime
import time
import json

class Okex2P2(MarketP2P):
    #urlv16 = 'https://www.okx.com/v3/c2c/tradingOrders/books?t='+time+'&quoteCurrency='+Fiat+'&baseCurrency='+Lot+'&side='+buysell+'&paymentMethod='+Paymethods+'&userType=all&showTrade=false&showFollow=false&showAlreadyTraded=false&isAbleFilter=false&urlId=0'
    #url = 'https://www.okx.com/v3/c2c/tradingOrders/books?t={0}&quoteCurrency={1}&baseCurrency={2}&side={3}&paymentMethod={4}&userType=all&showTrade=false&showFollow=false&showAlreadyTraded=false&isAbleFilter=false&sortType=price_{5}'
    url = 'https://www.okx.cab/v3/c2c/tradingOrders/books?t={0}&quoteCurrency={1}&baseCurrency={2}&side={3}&paymentMethod={4}&userType=all&showTrade=false&hideOverseasVerificationAds=false&showFollow=false&showAlreadyTraded=false&isAbleFilter=false&sortType={5}'
    header = {'User-Agent' : "PostmanRuntime/7.29.0", 'Accept':'*/*', 'Accept-Encoding':'gzip, deflate, br', 'Connection':'keep-alive'}
    PayMethodOkex = {
                     EPaymentMethodsOkexRUB.Tinkoff : "Tinkoff",
                     EPaymentMethodsOkexRUB.Raiffaizen : "Raiffaizen",
                     EPaymentMethodsOkexRUB.Rosbank : "Rosbank",
                     EPaymentMethodsOkexRUB.Sberbank : "Sberbank",
                     EPaymentMethodsOkexRUB.Alfa : "Alfa Bank",
                     EPaymentMethodsOkexRUB.Gazprombank : "Gazprombank",
                     EPaymentMethodsOkexRUB.Otkritie : "Otkritie",
                     EPaymentMethodsOkexRUB.VTB : "VTB",
                     EPaymentMethodsOkexRUB.SBP : "SBP Fast Bank Transfer",
                    }

    async def __getSeconds__(self):
        second = str(time.time())
        second = second[:len(second)-4]
        second = second.replace('.', '')
        return second

    async def __get_data_server__(self, Fiat:str, Lot:str, PayMethod, Operation:str, filter:int, session):
        try:
            PayMethod = self.PayMethodOkex.get(PayMethod)
            second = await self.__getSeconds__()
            if Operation.lower() == 'sell': 
                sort = 'asc'
                Operation = 'buy'
            else: 
                sort = 'desc'
                Operation = 'sell'
            if self._isUseProxy:
                responce = await session.get(self.url.format(second, Fiat, Lot, Operation, PayMethod, sort) + "&quoteMinAmountPerOrder="+str(filter), headers=self.header, proxy='http://{0}'.format(self._proxy.GetProxy()), timeout = self._ConnectionTimeout)
            else:
                responce = await session.get(self.url.format(second, Fiat, Lot, Operation, PayMethod, sort) + "&quoteMinAmountPerOrder="+str(filter), headers=self.header, timeout = self._ConnectionTimeout)                
            jdata = await responce.text(encoding="UTF-8")
            data = json.loads(jdata)['data']
            data = data[Operation]
            return data
        except Exception as e:
            print("{0} Error load data okex".format(datetime.today().strftime('%Y-%m-%d %H:%M:%S')), e, flush=True)
            return {}

    def __parsData__(self, data, minOrders):
        for lot in data:
            if self.name != lot['nickName'] and minOrders <= lot['completedOrderQuantity']:
                return lot['price']
        return "0"

    def __findMyPrice(self, data):
        for lot in data:
            if self.name == lot['nickName']:
                return lot['price']
        return "0"

    async def __ParseAllData__(self, data:list):
        parseData = []
        for lot in data:
            info = {}
            info.update({"name" : lot['nickName']})
            info.update({"orders" : lot['completedOrderQuantity']})
            info.update({"price" : lot['price']})
            info.update({"finishRate" : lot['completedRate']})
            info.update({"surplusAmount" : lot['availableAmount']})
            info.update({"minSingleTransAmount" : lot['quoteMinAmountPerOrder']})
            info.update({"maxSingleTransAmount" : lot['quoteMaxAmountPerOrder']})
            parseData.append(info)
        return parseData

    def GetBestPrice(self, PaymentMethods: Enum, Fiat: Enum, Lot: Enum, Operation: Enum, Filter: int, MinOrders: int):
        data =  self.__get_data_server__(Fiat.name, Lot.name, PaymentMethods, Operation.name.lower(), Filter)
        return self.__parsData__(data, MinOrders)

    def GetMyPrice(self, PaymentMethods: Enum, Fiat: Enum, Lot: Enum, Operation: Enum, Filter: int, maxPages: int):
        if self.name == "":
            return "0"
        data = self.__get_data_server__(Fiat.name, Lot.name, PaymentMethods, Operation.name.lower(), Filter)
        return self.__findMyPrice(data)

    async def GetAllTickets(self, PaymentMethods: Enum, Fiat: Enum, Lot: Enum, Operation: Enum, maxPages: int, session) -> list:
        parseData = {}
        data = []
        temp = await self.__get_data_server__(Fiat.name, Lot.name, PaymentMethods, Operation.name.lower(), 0, session)
        data = await self.__ParseAllData__(temp)
        parseData.update({'data': data})
        parseData.update({'fiat': Fiat.name})
        parseData.update({'payMethod': PaymentMethods.name})
        parseData.update({'lot': Lot.name})
        return parseData