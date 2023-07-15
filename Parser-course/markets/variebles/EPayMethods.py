from enum import Enum

#Binance
class EpaymentMethodsBinanceRUB(Enum):
    TinkoffNew = 1
    RosBankNew = 2
    RaiffeisenBank = 3
    HomeCreditBank = 4
    PostBankNew = 5
    QIWI = 6

class EpaymentMethodsBinanceUSD(Enum):
    BankofGeorgia = 1

class EpaymentMethodsBinanceGEL(Enum):
    BankofGeorgia = 1

class EpaymentMethodsBinanceKZT(Enum):
    KaspiBank = 1
    HalykBank = 2
    CenterCreditBank = 3

#Huobi 
class EPaymentMethodsHuobiRUB(Enum):
    Tinkoff = 28
    Raiffaizen = 36
    Rosbank = 358
    HomeCredit = 172
    PostBank = 357
    Sberbank = 29
    Alfa = 25
    Gazprombank = 351
    Otkritie = 103
    SovcomBank = 361
    RosselhozBank = 359
    SPB = 69
    VTB = 27

#OKX
class EPaymentMethodsOkexRUB(Enum):
    Tinkoff = 1
    Raiffaizen = 2
    Rosbank = 3
    Sberbank = 4
    Alfa = 5
    Gazprombank = 6
    Otkritie = 7
    VTB = 8
    SBP = 9

#Pexpay
class EPaymentMethodsPaxpayRUB(Enum):
    Sberbank = 1
    RaiffeisenBankRussia = 2
    AlfaBank = 3
    Tinkoff = 4
    VTB = 5
    SBP = 6

#ByBit
class EPaymentMethodsByBitRUB(Enum):
    Rosbank = 185
    UralsibBank = 271
    AlfaBank = 379
    Tinkoff = 75
    VTB = 381
    RaiffeisenBank = 64