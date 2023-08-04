from flask import Flask, request, render_template, make_response
import requests
import json

app = Flask(__name__)

@app.route('/', methods = ['GET'])
def main_page():
    return make_response(render_template("main.html"))

@app.route("/contact", methods = ["GET"])
def contact():
    return "Hello world!"

@app.route("/reviews", methods = ["GET"])
def reviews():
    return "Hello world!"

@app.route("/bid", methods = ["POST"])
def bid():
    responce = requests.post(url = "http://exchanger-data:9000/bid", json=request.json)
    jsdata = responce.json()
    if jsdata.get("resualt") == False:
        return "Errror"
    order_id = jsdata.get("OrderID")
    data = jsdata.get("data")
    responce = make_response(render_template("bid.html", oreder_number = order_id, 
                                         price = data.get("price"), payMethod = data.get("pay_type"),
                                         order_pay = data.get("bank_number"), order_name = data.get("bank_owner_name"), number_payMethod = data.get("setter_number"), 
                                         order_count = data.get("count"), number_getter = data.get("wallet")))
    responce.set_cookie("OrderID", order_id)
    return responce

if __name__ == "__main__":
    app.run("0.0.0.0", port=5010)