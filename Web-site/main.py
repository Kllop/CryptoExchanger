from flask import Flask, request, render_template, make_response, jsonify
import requests
import json

app = Flask(__name__)

@app.route('/', methods = ['GET'])
def main_page():
    return make_response(render_template("index.html"))

@app.route("/my-bids", methods = ["GET"])
def bids():
    return make_response(render_template("my-bids.html"))

@app.route("/rules", methods = ["GET"])
def rules():
    return make_response(render_template("rules.html"))

@app.route("/faq", methods = ["GET"])
def faq():
    return make_response(render_template("faq.html"))

@app.route("/contacts", methods = ["GET"])
def contacts():
    return make_response(render_template("contacts.html"))

@app.route("/bid", methods = ["GET"])
def bid_page():
    # запрос на получение заявки
    # responce = requests.post(url = "http://exchanger-data:9000/bid", json=request.json)
    # заглушка заявки
    response = {"resualt" : True, "OrderID" : "Hello", "data" : {"price" : "10000", "bank_name" : "Tinkoff RUB", "bank_number" : "1232132312", "bank_owner_name" : "Алексей К.", "setter_number" : "4276290058654584", "pay_type" : "Тинькофф", "count" : "20", "wallet" : "btcwallet0021", "coin" : "BTC"}}
    jsdata = response
    if jsdata.get("resualt") == False:
        return "Errror"
    order_id = jsdata.get("OrderID")
    data = jsdata.get("data")
    responce = make_response(render_template("bid.html", oreder_number=order_id,
                                             price=data.get("price"), payMethod=data.get("pay_type"),
                                             order_pay=data.get("bank_number"), order_name=data.get("bank_owner_name"),
                                             number_payMethod=data.get("setter_number"),
                                             order_count=data.get("count"), number_getter=data.get("wallet")))
    return responce

@app.route("/bid", methods = ["POST"])
def bid():
    responce = requests.post(url = "http://exchanger-data:9000/bid", json=request.json)
    jsdata = responce.json()
    if jsdata.get("resualt") == False:
        return "Errror"
    order_id = jsdata.get("OrderID")

    responce = make_response(jsonify({'success': 1}), 201)
    responce.set_cookie("OrderID", order_id)
    return responce

if __name__ == "__main__":
    app.run("0.0.0.0", port=5010)