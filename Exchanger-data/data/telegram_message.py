import requests

class TelegramMessage:
    
    def __init__(self) -> None:
        self.TeleBot = '6163052051:AAHpUAmWaU9Vlf71kyAZ-brg2fet_CUvx0E'
        self.chatID = '5829831042'
    
    def __sendMessage__(self, message:str):   
        requests.get("https://api.telegram.org/bot{0}/sendMessage?chat_id={1}&text={2}".format(self.TeleBot, self.chatID, message))

    def sendOrderInfo(self, order_data:dict) -> None:
        message = """Покупатель оплатил ордер № {0} {1} на сумму {2} RUB, переведите {3} в количестве {4} на адрес {5} **********************\ntelegram : {6}, курс {7}""".format(
            order_data.get("orderID"), order_data.get("pay_type"), order_data.get("price"), order_data.get("coin"), order_data.get("count"), 
            order_data.get("wallet"), order_data.get("telegram"), order_data.get("course"))
        self.__sendMessage__(message)

    def sendNewOrder(self) -> None:
        self.__sendMessage__("У вас новая заявка")

    def sendCencelOder(self) -> None:
        self.__sendMessage__("Ордер отменен")