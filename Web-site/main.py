from flask import Flask, request, render_template, make_response, jsonify, redirect
import requests
import json

app = Flask(__name__)

@app.route('/', methods = ['GET'])
def main_page():
    return make_response(render_template("index.html"))

@app.route("/my-bids", methods = ["GET"])
def bids():
    return redirect("bid")
    #return make_response(render_template("my-bids.html"))

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
    order_id = request.cookies.get("OrderID")
    responce = requests.post(url = "http://exchanger-data:9000/order", json={"order_id" : order_id})
    jsdata = responce.json()
    if jsdata.get("resualt") == False:
        return "Errror"
    data = jsdata.get("data")
    responce = make_response(render_template("bid.html", oreder_number=data.get("orderID"),
                                             price=data.get("price"), payMethod=data.get("pay_type"),
                                             order_pay=data.get("bank_number"), order_name=data.get("bank_owner_name"),
                                             number_payMethod=data.get("setter_number"), change_time = data.get("change_time"),
                                             order_count=data.get("count"), number_getter=data.get("wallet")))
    return responce

@app.route("/bid", methods = ["POST"])
def bid():
    responce = requests.post(url = "http://exchanger-data:9000/bid", json=request.json)
    jsdata = responce.json()
    if jsdata.get("resualt") == False:
        return "Errror"
    order_id = str(jsdata.get("OrderID"))
    responce = make_response(jsonify({'success': 1}), 201)
    responce.set_cookie("OrderID", order_id)
    return responce

if __name__ == "__main__":
    app.run("0.0.0.0", port=5010)