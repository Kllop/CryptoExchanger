from binance.spot import Spot

class BinanceSpot:
    __client = None

    def __init__(self, key:str, secret:str):
        self.__client = Spot(api_key=key, api_secret=secret)
    
    def GetPrice(self, lot:str) -> str:
        price = " "
        try:
            price = self.__client.ticker_price(lot)
        except Exception:
            print("Error not found " + lot + " ticker")
            return {'coin' : lot, 'price' : "0.00"}
        return {'coin' : lot, 'price' : price['price']}

    def GetPrices(self, binanceSpotLots:list) -> list:
        data = []
        for lot in binanceSpotLots:
            data.append(self.GetPrice(lot))
        return data