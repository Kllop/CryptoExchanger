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
    print(request.json)
    return "Ok", 200


if __name__ == "__main__":
    app.run("0.0.0.0", port=5010)