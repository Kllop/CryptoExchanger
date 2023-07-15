from markets.market import MarketSpot

class HuobiSpot(MarketSpot):

    def __init__(self, isUseProxy=False, ConnectionTimeout=5) -> None:
        super().__init__(isUseProxy, ConnectionTimeout)
        self._url = 'https://api.huobi.pro/market/tickers'

    async def __ParsData__(self, data:dict) -> list:
        temp = []
        for ticket in data:
            coin = ticket['symbol']
            price = ticket['ask']
            temp.append({'coin' : coin.upper(), 'price' : price})
        return temp