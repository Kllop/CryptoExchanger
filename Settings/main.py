from flask import Flask
from Database.db_redis import Redis_DB
from Database.db_postgres import Postgres_DB
import json

app = Flask(__name__)
redis_db = Redis_DB()
postgres_db = Postgres_DB("ownerdb", "X$Oi815H%nd*FLyB!9v%", "postgres-data", "5432", "exchange")

@app.route('/admin')
def admin():
    return "Hello"

@app.route('/owner')
def owner():
    return "Hello"

@app.route("/operator")
def operator():
    return "Hello"

coin_and_pay = {
                "BTC" : [{"name_en" : "Sberbank", "name_ru" : "Сбербанк RUB", "percent" : 5.00}, 
                         {"name_en" : "Alfabank", "name_ru" : "Альфабанк RUB", "percent" : 2.00}, 
                         {"name_en" :"Tinkoff", "name_ru" : "Тинькофф RUB", "percent" : 3.00}],

                "ETH" : [{"key" : "Sberbank", "name" : "Сбербанк RUB"}, 
                         {"key" : "Alfabank", "name" : "Альфабанк RUB"}, 
                         {"key" :"Uralsib", "name" : "Уралсиб RUB"}]
                }

def createDirection():
    postgres_db.SendDirectoion("ETH", "TinkoffNew", "Тинькофф RUB", "Tinkoff RUB", "Tinkoff", 5.00, "P2P")
    postgres_db.SendDirectoion("USDT", "TinkoffNew", "Тинькофф RUB", "Tinkoff RUB", "Tinkoff", 5.00, "P2P")

def setReidsDirection():
    postgre_data = postgres_db.GetDirection()
    redis_db.removeKey("tradepreference")
    for data in postgre_data:
        send_data = {"coin" : data[0], "name_exch" : data[1], "name_ru" : data[2], "name_en" : data[3], "name_des" : data[4], "percent" : data [5], "market" : data[6]}
        redis_db.setValueList("tradepreference", json.dumps(send_data))

if __name__ == "__main__":
    setReidsDirection()
    app.run("0.0.0.0", port=9010)