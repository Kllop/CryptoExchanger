import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class Sender_Email:

    port = 465
    smtp_server = "smtp.yandex.ru"
    sender_email = "Jango.Exchange@yandex.ru"
    password = "sdiluwezapcsrbcr"
    context = ssl.create_default_context()

    def send_order_email(self, receiver_email:str, direction_to:str, direction_from:str, summ:str, coin_count:str, coin:str, wallet:str):
        message = MIMEMultipart("alternative")
        message["Subject"] = "Новая заявка"
        message["From"] = self.sender_email
        message["To"] = receiver_email

        # Create the plain-text and HTML version of your message
        text = """\
        Вы оформили заявку на обмена, на сайте https://jango-exchange.com/
        -----------------------------------------------------------------
        Детали заявки
        Направление : {0} -> {1}
        Cумма к оплате : {2} РУБ
        Вы получите : {3} {4}
        Счет получения : {5}
        ------------------------------------------------------------------
        Контакты для связи :
        Email : Jango.Exchange@yandex.ru
        Telegram : @Jango_Exchange
        """.format(direction_to, direction_from, summ, coin_count, coin, wallet) #Tinkoff -> USDT(TRC20)

        part1 = MIMEText(text, "plain")

        message.attach(part1)

        self.__send_email__(message, receiver_email)
    
    def __send_email__(self, message, receiver_email):
        with smtplib.SMTP_SSL(self.smtp_server, self.port, context=self.context) as server:
            server.login(self.sender_email, self.password)
            server.sendmail(self.sender_email, receiver_email, message.as_string())