from markets.market import MarketSpot

class OkexSpot(MarketSpot):

    def __init__(self, isUseProxy=False, ConnectionTimeout=5) -> None:
        super().__init__(isUseProxy, ConnectionTimeout)
        self._url = 'https://www.okx.com/api/v5/market/tickers?instType=SPOT'

    async def __ParsData__(self, data:dict) -> list:
        temp = []
        for ticket in data:
            coin = ticket['instId'].replace('-', '')
            price = ticket['last']
            temp.append({'coin' : coin.upper(), 'price' : price})
        return temp
