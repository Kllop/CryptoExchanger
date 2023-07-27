class Preference:

    PayMethodsBinance = {"Tinkoff" : "TinkoffNew", 
           "Sberbank" : "RosBankNew",
           "Raiffeisen" : "RaiffeisenBank",
           "HomeCredit" : "HomeCreditBank",
           "PostBank" : "PostBankNew"
           }
    
    COINS = ["USDT","BTC","BUSD","BNB","ETH","SHIB"]

    PayMethodDescription = {"Tinkoff" : "Тинькофф",
                            "Sberbank" : "Сбербанк",
                            "Raiffeisen" : "Райфайзен",
                            "HomeCredit" : "Хомкредит",
                            "PostBank" : "ПочтаБанк"
                            }
    
    Exchanges = ["Binance"]

    ###Table postger 
    # coin = BTC,
    # payMethodExchange = "TinkoffNew", 
    # payMethodRU = "Тинькофф", 
    # payMethodEN = "Tinkoff", 
    # Exchange = "Binance"