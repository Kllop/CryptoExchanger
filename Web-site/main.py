from flask import Flask, request, render_template, make_response, jsonify, redirect, session, Response
from werkzeug.middleware.proxy_fix import ProxyFix
import requests

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

@app.route('/', methods = ['GET'])
def main_page():
    GetIp()
    code_id = request.args.get('id')
    responce = make_response(render_template("index.html"))
    if code_id != None:
        responce.set_cookie("referal", code_id)
    return responce

@app.route('/log', methods = ['GET'])
def log():
    if session.get('id') != None:
        print("Login in", flush=True)
    return make_response(render_template("log.html"))

@app.route('/reg', methods = ['GET'])
def reg():
    if session.get('id') != None:
        print("Registration", flush=True)
    return make_response(render_template("reg.html"))

@app.route("/my-bids", methods = ["GET"])
def bids():
    return redirect("bid")
    #return make_response(render_template("my-bids.html"))

@app.route("/referal", methods = ["GET"])
def referal():
    code_id = session.get('id')
    if code_id == None:
        return {}
    responce = requests.post(url = "http://exchanger-data:9000/referal", json={"id" : code_id})
    return responce.json()

@app.route("/rules", methods = ["GET"])
def rules():
    return make_response(render_template("rules.html"))

@app.route("/faq", methods = ["GET"])
def faq():
    return make_response(render_template("faq.html"))

@app.route("/contacts", methods = ["GET"])
def contacts():
    return make_response(render_template("contacts.html"))

@app.route("/status", methods = ["GET"])
def status():
    order_id = request.cookies.get("OrderID")
    if order_id == None:
        return redirect("/")
    responce = requests.post(url = "http://exchanger-data:9000/status", json={"key" : order_id, "status" : request.args.get("status")})
    return responce.json()

@app.route("/bid", methods = ["GET"])
def bid_page():
    order_id = request.cookies.get("OrderID")
    if order_id == None:
        return redirect("/")
    responce = requests.post(url = "http://exchanger-data:9000/order", json={"order_id" : order_id})
    jsdata = responce.json()
    if jsdata.get("resualt") == False:
        return "Errror"
    data = jsdata.get("data")
    isNewStatus = data.get("status") == "new order"
    responce = make_response(render_template("bid.html", oreder_number=data.get("orderID"),
                                             price=data.get("price"), payMethod=data.get("pay_type"),
                                             order_pay=data.get("bank_number"), order_name=data.get("bank_owner_name"),
                                             number_payMethod=data.get("setter_number"), change_time = data.get("change_time"),
                                             order_count=data.get("count"), number_getter=data.get("wallet"), isNewStatus = isNewStatus))
    return responce

def getReferalCode():
    out = request.cookies.get('referal')
    if out == None:
        return ""
    return out

def GetIp():
    #ip =  request.environ.get('HTTP_X_REAL_IP', request.remote_addr) 
    print(request.remote_addr, flush=True)
    return "ip"

@app.route("/registration", methods = ["POST"])
def registration():
    jsdata = request.json
    referal = getReferalCode()
    responce = requests.post(url = "http://exchanger-data:9000/registration", json={"login" : jsdata.get('login'), "password" : jsdata.get('password'),
                                                                                    "email" : jsdata.get('email'), "referal" : referal, 
                                                                                    "ip" : "127.0.0.1"})
    outdata = responce.json()
    if outdata.get('resualt') == True:
        session['id'] = outdata.get('id')
    return {"resualt" : outdata.get('resualt'), "message" : outdata.get('message')}

@app.route("/authorization", methods = ["POST"])
def authorization():
    jsdata = request.json
    responce = requests.post(url = "http://exchanger-data:9000/authorization", json={"login" : jsdata.get('login'), "password" : jsdata.get('password'), 
                                                                                     "ip" : "127.0.0.1"})
    outdata = responce.json()
    if outdata.get('resualt') == True:
        session['id'] = outdata.get('id')
    return {"resualt" : outdata.get('resualt')}

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

@app.route("/direction", methods = ["GET"])
def direction():
    responce = requests.get(url = "http://exchanger-data:9000/direction")
    return responce.json()

@app.route("/course", methods = ["GET"])
def course():
    responce = requests.get(url = "http://exchanger-data:9000/course")
    return responce.json()

@app.route("/request-exportxml.xml", methods = ["GET"])
def request_exportxml():
    responce = requests.get(url = "http://exchanger-data:9000/request-exportxml.xml")
    return Response(responce.content, mimetype='text/xml')

if __name__ == "__main__":
    app.run("0.0.0.0", port=5010)