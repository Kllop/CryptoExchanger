from flask import Flask, request, render_template, make_response
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
    return "Ok"
    #return make_response(render_template("bid.html", oreder_number = 1, 
    #                                     price = 10000, payMethod = "Тинькофф RUB",
    #                                     order_pay = "1231232131", order_name = "Алексей К.", number_payMethod = jsdata['setterNumber'], 
    #                                     order_count = jsdata['getterValue'], number_getter = jsdata['getterNumber']))
if __name__ == "__main__":
    app.run("0.0.0.0", port=5010)