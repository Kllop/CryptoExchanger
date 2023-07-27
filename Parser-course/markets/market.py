from proxy import Proxy, proxyListSpot
from enum import Enum
import json
import aiohttp

class MarketP2P:

    def __init__(self, name:str = "", isUseProxy = False, ConnectionTimeout = 5, proxyList = []) -> None:
        self._name = name
        self._isUseProxy = isUseProxy
        self._ConnectionTimeout = ConnectionTimeout
        if isUseProxy:
            self._proxy = Proxy(proxyList)


    def GetAllTickets(self, PaymentMethods:Enum, Fiat:Enum, Lot:Enum, Operation:Enum, maxPages:int) -> dict:
        pass

    def GetBestPrice(self, PaymentMethods:Enum, Fiat:Enum, Lot:Enum, Operation:Enum, Filter:int, MinOrders:int) -> str:
        pass

    def GetMyPrice(self, PaymentMethods:Enum, Fiat:Enum, Lot:Enum, Operation:Enum, Filter:int, maxPages:int) -> str:
        pass

    def getAllBestPrices(self, PaymentMethods:Enum, Coins:Enum, Fiat:Enum, Operation:Enum, Filter:int, MinOrders:int) -> list[str]:
        data = []
        for Coin in Coins.mro()[0]:
            data.append(self.GetBestPrice(PaymentMethods, Fiat, Coin, Operation, Filter, MinOrders))
        return data

    def getAllMyPrices(self, PaymentMethods:Enum, Coins:Enum, Fiat:Enum, Operation:Enum, Filter:int, maxPages:int) -> list[str]:
        data = []
        for Coin in Coins.mro()[0]:
            data.append(self.GetMyPrice(PaymentMethods, Fiat, Coin, Operation, Filter, maxPages))
        return data

    def GetCoins(self, typeCoin:Enum) -> list[str]:
        data = []
        for temp in typeCoin.mro()[0]:
            data.append(temp.name + "/RUB")
        return data

class MarketSpot:
    _url = ''

    def __init__(self, isUseProxy = False, ConnectionTimeout = 5) -> None:
        self._header = {'User-Agent' : "PostmanRuntime/7.29.0", 'Accept':'*/*', 'Accept-Encoding':'gzip, deflate', 'Connection':'keep-alive'}
        self._isUseProxy = isUseProxy
        self._ConnectionTimeout = ConnectionTimeout
        if isUseProxy:
            self._proxy = Proxy(proxyListSpot)

    async def __getDataServer__(self):
        async with aiohttp.ClientSession() as session:
            try:
                if self._isUseProxy:
                    response = await session.get(self._url, headers=self._header,  proxy = 'http://{0}'.format(self._proxy.GetProxy()), timeout = self._ConnectionTimeout)
                else:
                    response = await session.get(url = self._url, headers=self._header, timeout = self._ConnectionTimeout)
                jsdata = await response.text(encoding="UTF-8")
                data = json.loads(jsdata)['data']
                return data
            except Exception as e:
                print(e.args, e.__traceback__, __name__,  flush=True)
                return []

    async  def __ParsData__(self, data:dict) -> list:
        pass

    async def GetPrices(self):
        data = await self.__getDataServer__()
        return await self.__ParsData__(data)

