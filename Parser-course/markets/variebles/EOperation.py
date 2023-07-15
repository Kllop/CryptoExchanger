from enum import Enum

class EOperation(Enum):
    BUY = 1
    SELL = 0

#Binance
class EOperationBinance(Enum):
    BUY = 1
    SELL = 2

#Huobi
class EOperationHuobi(Enum):
    buy = 1
    sell = 2

#OKX
class EOperationOkex(Enum):
    buy = 1
    sell = 2

#Pexpay
class EOperationPexpay(Enum):
    BUY = 1
    SELL = 2
