from Database.db_postgres import Postgres_DB

class Commission:

    data = {"BTC"  : {'low': 20, "mid" : 25, "high" : 30},
            "ETH"  : {'low': 17, "mid" : 18, "high" : 20},
            "USDT" : {'low': 1, "mid" : 1, "high" : 1}}

    def __init__(self) -> None:
        self.db = Postgres_DB("ownerdb", "X$Oi815H%nd*FLyB!9v%", "postgres-data", "5432", "exchange")

    def send_commission(self, commission:dict) -> None:
        self.data = commission
    
    def get_commission(self) -> dict:
        return self.data