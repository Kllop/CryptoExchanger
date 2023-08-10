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

def createDirection():
    postgres_db.DropTable("DirectionPreference")
    postgres_db.ClearTable("DirectionPreference")
    postgres_db.SendDirectoion("BTC", "TinkoffNew", "Тинькофф RUB", "Tinkoff RUB", "Tinkoff", 5.00, "P2P")
    postgres_db.SendDirectoion("BTC", "TinkoffNew", "Альфабанк RUB", "Alfabank RUB", "Alfabank", 5.00, "P2P")
    postgres_db.SendDirectoion("ETH", "TinkoffNew", "Тинькофф RUB", "Tinkoff RUB", "Tinkoff", 5.00, "P2P")
    postgres_db.SendDirectoion("ETH", "TinkoffNew", "Альфабанк RUB", "Alfabank RUB", "Alfabank", 5.00, "P2P")
    postgres_db.SendDirectoion("USDT", "TinkoffNew", "Тинькофф RUB", "Tinkoff RUB", "Tinkoff", 5.00, "P2P")
    postgres_db.SendDirectoion("USDT", "TinkoffNew", "Альфабанк RUB", "Alfabank RUB", "Alfabank", 5.00, "P2P")

def setReidsDirection():
    postgre_data = postgres_db.GetDirection()
    redis_db.removeKey("tradepreference")
    for data in postgre_data:
        send_data = {"coin" : data[0], "name_exch" : data[1], "name_ru" : data[2], "name_en" : data[3], "name_des" : data[4], "percent" : data [5], "market" : data[6]}
        redis_db.setValueList("tradepreference", json.dumps(send_data))

@app.route("/allorders")
def allOrders():
    return postgres_db.GetAllOrders()

if __name__ == "__main__":
    createDirection()
    setReidsDirection()
    app.run("0.0.0.0", port=9010)