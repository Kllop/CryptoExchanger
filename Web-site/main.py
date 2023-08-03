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
    data = responce.json
    print(data)
    return make_response(render_template("bid.html", oreder_number = 1, 
                                         price = 10000, payMethod = "Тинькофф RUB",
                                         order_pay = "1231232131", order_name = "Алексей К.", number_payMethod = 312312, 
                                         order_count = 23123, number_getter = 312321))

if __name__ == "__main__":
    app.run("0.0.0.0", port=5010)