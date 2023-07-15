from markets.market import MarketSpot

class PexpaySpot(MarketSpot):
    
    def __init__(self, isUseProxy=False, ConnectionTimeout=5) -> None:
        super().__init__(isUseProxy, ConnectionTimeout)
        self._url = 'https://www.pexpay.com/bapi/mbx/v1/public/spot/config/symbols'
    
    async  def __ParsData__(self, data:dict) -> list:
        temp = []
        for ticket in data:
            coin = ticket['s']
            price = ticket['c']
            temp.append({'coin' : coin.upper(), 'price' : price})
        return temp
