from flask import Flask, request, render_template, make_response
from requests import request
import json

app = Flask(__name__)

json_export_course = {"BTC" : {"Sberbank" : "2950000", "Alfabank" : "3000000", "Tinkoff" : "2900000"}, 
                      "ETH" : {"Sberbank" : "185000", "Alfabank" : "187000", "Uralsib" : "186500"}}

@app.route('/', methods = ['GET'])
def main_page():
    payMethds = request("GET", "")
    return make_response(render_template("main.html"))

@app.route("/contact", methods = ["GET"])
def contact():
    return "Hello world!"

@app.route("/reviews", methods = ["GET"])
def reviews():
    return "Hello world!"

@app.route("/bid", methods = ["POST"])
def bid():
    print(request.json)
    return "Ok", 200

@app.route("/course", methods = ["GET"])
def course():
    return json.dumps(json_export_course)

@app.route("/data", methods = ["GET"])
def data():
    return ""

@app.route("/offers", methods = ["GET"])
def offers():
    return json.dumps(coin_and_pay)

if __name__ == "__main__":
    app.run("127.0.0.1", 5010)