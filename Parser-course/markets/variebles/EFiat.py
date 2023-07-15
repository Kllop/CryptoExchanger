from enum import Enum

#Binance
class EFiatBinance(Enum):
    RUB = 1
    USD = 2
    GEL = 3
    KZT = 4

#Huobi
class EFiatHuobi(Enum):
    rub = 11

#OKX
class EFiatOkex(Enum):
    rub = 1

#Pexpay
class EFiatPaxpay(Enum):
    RUB = 1

class EFiatByBit(Enum):
    RUB = 1