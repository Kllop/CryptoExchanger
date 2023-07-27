from flask import Flask
from Database.db_redis import Redis_DB
import json

app = Flask(__name__)
redis_db = Redis_DB()

@app.route('/admin')
def admin():
    return "Hello"

@app.route('/owner')
def owner():
    return "Hello"

@app.route("/operator")
def operator():
    return "Hello"

if __name__ == "__main__":
    data = [json.dumps({"coin" : "BTC", "exhcange" : "Binance", "payMethodExchange" : "TinkoffNew", "payMethodRU" : "Тинькофф", "market" : "P2P"}),
            json.dumps({"coin" : "ETH", "exhcange" : "Binance", "payMethodExchange" : "TinkoffNew", "payMethodRU" : "Тинькофф", "market" : "P2P"}),
            json.dumps({"coin" : "USDT", "exhcange" : "Binance", "payMethodExchange" : "TinkoffNew", "payMethodRU" : "Тинькофф", "market" : "P2P"})
           ]
    redis_db.removeKey("tradepreference")
    for temp in data:
        redis_db.setValueList("tradepreference", temp)   
    app.run("0.0.0.0", port=5010)