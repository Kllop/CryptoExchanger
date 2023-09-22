from flask import Flask, request, render_template, make_response, jsonify, redirect, session, Response
from werkzeug.middleware.proxy_fix import ProxyFix
import requests
import datetime

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=2)
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
    code_id = request.args.get('ref')
    responce = make_response(render_template("index.html"))
    if code_id != None:
        expire_date = datetime.datetime.now()
        expire_date = expire_date + datetime.timedelta(days=365)
        responce.set_cookie("referal", code_id, expires=expire_date)
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

def referal_code():
    code_id = session.get('id')
    print(code_id)
    if code_id == None:
        return {}
    responce = requests.post(url = "http://exchanger-data:9000/referalcode", json={"id" : code_id})
    return responce.json()

def referal_bid():
    code_id = session.get('id')
    if code_id == None:
        return {}
    responce = requests.post(url = "http://exchanger-data:9000/referalbid", json={"id" : code_id})
    return responce.json()

def referal_count():
    code_id = session.get('id')
    if code_id == None:
        return {}
    responce = requests.post(url = "http://exchanger-data:9000/countreferal", json={"id" : code_id})
    return responce.json()

def all_my_bid():
    code_id = session.get('id')
    if code_id == None:
        return {}
    responce = requests.post(url = "http://exchanger-data:9000/allmybids", json={"id" : code_id})
    return responce.json()

@app.route("/rules", methods = ["GET"])
def rules():
    return make_response(render_template("rules/base.html"))

@app.route("/faq", methods = ["GET"])
def faq():
    return make_response(render_template("faq/base.html"))

@app.route("/contacts", methods = ["GET"])
def contacts():
    return make_response(render_template("contacts/base.html"))

@app.route("/account", methods = ["GET"])
def account():
    if session.get('session') != None:
        return redirect("/")
    referal = referal_code()
    count = referal_count()
    data = referal_bid()
    return make_response(render_template("account/base.html", referal_code = referal.get('referal'), count = count.get('count'), referal_bid = data.get('data')))

@app.route("/account-bids", methods = ["POST"])
def account_bids():
    data = all_my_bid()
    return make_response(render_template("account/bids.html", my_bids = data))

@app.route("/account-referral-program", methods = ["POST"])
def account_referral():
    data = referal_code()
    return make_response(render_template("account/referral-program/base.html", referal_code = data.get('referal')))

@app.route("/account-security", methods = ["POST"])
def account_security():
    return make_response(render_template("account/security.html"))

@app.route("/account-referral-referrals", methods = ["POST"])
def account_referrals():
    data = referal_count()
    return make_response(render_template("account/referral-program/referral-list.html", count = data.get('count')))

@app.route("/account-referral-charges", methods = ["POST"])
def account_charges():
    # TODO из-за этой строчки возвращает 500
    data = referal_bid()
    return make_response(render_template("account/referral-program/charges.html", referal_bid = data.get('data')))

@app.route("/account-referral-withdrawal", methods = ["POST"])
def account_withdrawal():
    return make_response(render_template("account/referral-program/withdrawal.html"))

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
    responce = make_response(render_template("bid-status/bid.html", oreder_number=data.get("orderID"),
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
    return request.remote_addr

def GetId():
    outdata = session.get('id')
    if outdata == None:
        return ""
    return outdata

@app.route("/registration", methods = ["POST"])
def registration():
    jsdata = request.json
    ip = GetIp()
    referal = getReferalCode()
    responce = requests.post(url = "http://exchanger-data:9000/registration", json={"login" : jsdata.get('login'), "password" : jsdata.get('password'),
                                                                                    "email" : jsdata.get('email'), "referal" : referal, "ip" : ip})
    outdata = responce.json()
    if outdata.get('resualt') == True:
        session['id'] = outdata.get('id')
    return {"resualt" : outdata.get('resualt'), "message" : outdata.get('message')}

@app.route("/authorization", methods = ["POST"])
def authorization():
    jsdata = request.json
    ip = GetIp()
    responce = requests.post(url = "http://exchanger-data:9000/authorization", json={"login" : jsdata.get('login'), "password" : jsdata.get('password'), "ip" : ip})
    outdata = responce.json()
    if outdata.get('resualt') == True:
        session['id'] = outdata.get('id')
    return {"resualt" : outdata.get('resualt')}

@app.route("/bid", methods = ["POST"])
def bid():
    jsdata = request.json
    owner = GetId()
    if owner == None:
        owner = ""
    referal = getReferalCode()
    jsdata.update({"owner" : owner, "referal" : referal})
    responce = requests.post(url = "http://exchanger-data:9000/bid", json=jsdata)
    jsdata = responce.json()
    if jsdata.get("resualt") == False:
        return "Errror"
    order_id = str(jsdata.get("OrderID"))
    responce = make_response(jsonify({'success': 1}), 201)
    responce.set_cookie("OrderID", order_id)
    return responce

@app.route("/logout", methods = ["GET"])
def logout():
    session.pop('id')
    print('logout', flush=True)
    return {'resualt' : True}

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


################## ADMIN #######################

def getAdminId():
    return session.get("admin_id")

@app.route("/jango_admin", methods = ["GET"])
def admin_page():
    return make_response(render_template("admin/login_admin.html"))

@app.route("/jango_admin", methods = ["POST"])
def admin_login():
    jsdata = request.json
    responce = requests.post(url = "http://settings-data:9010/admin_login", json={"login" : jsdata.get("login") , "password" : jsdata.get("password")})
    outjson = responce.json()
    resualt = outjson.get('resualt')
    if resualt == True:
        user_id = outjson.get('id')
        uid_chat = outjson.get('uuid')
        session.update({"admin_id" : user_id})
    return {"resualt" : resualt}

def get_all_orders(user_id):
    responce = requests.post(url = "http://settings-data:9010/all_orders", json={"id" : user_id})
    return responce.json()

def get_order_detail(user_id):
    order_id = request.args.get('id')
    responce = requests.post(url = "http://settings-data:9010/order_detail", json={"id" : user_id, "order_id" : order_id})
    return responce.json()

############### DIRECTION ################

def get_all_direction(user_id):
    responce = requests.post(url = "http://settings-data:9010/all_direction", json={"id" : user_id})
    return responce.json()

def remove_direction(user_id, data:dict):
    uid = data.get('uid')
    responce = requests.post(url = "http://settings-data:9010/remove_direction", json={"id" : user_id, "order_id" : uid})
    return responce.json()

def create_direction(user_id:str, data:dict):
    coin = data.get("coin")
    pay_method = data.get("pay_method")
    bank_ru = data.get("bank_ru")
    bank_en = data.get("bank_en")
    bank_ind = data.get("bank_ind")
    percent = data.get("percent")
    area = data.get("area")
    market = data.get("market")
    responce = requests.post(url = "http://settings-data:9010/create_direction", json={"id" : user_id, "coin" : coin, "pay_method" : pay_method, 
                                                                                       "bank_ru" : bank_ru, "bank_en" : bank_en, "bank_ind" : bank_ind, 
                                                                                       "percent" : percent, "area" : area, "market" : market})
    return responce.json()

########## METHODS #########

@app.route("/all_direction", methods = ["GET"])
def direction_method():
    user_id = getAdminId()
    if user_id == None:
        return redirect("/")
    data = get_all_direction(user_id)
    if data.get("resualt") == False:
        session.pop("admin_id")
        return redirect("/")
    return {"data" : data.get('data')}

@app.route("/remove_direction", methods = ["POST"])
def remove_direction_method():
    user_id = getAdminId()
    if user_id == None:
        session.pop("admin_id")
        return redirect("/")
    outjson = remove_direction(user_id, request.json())
    resualt = outjson.get('resualt')
    return {"resualt" : resualt}

@app.route("/create_direction", methods = ["POST"])
def create_direction_method():
    user_id = getAdminId()
    if user_id == None:
        session.pop("admin_id")
        return redirect("/")
    outjson = create_direction(user_id, request.json())
    resualt = outjson.get('resualt')
    return {"resualt" : resualt}

#########################################################################################

@app.route("/order_panel", methods = ["GET"])
def orders():
    user_id = getAdminId()
    if user_id == None:
        return redirect("/")
    data = get_all_orders(user_id)
    if data.get("resualt") == False:
        session.pop("admin_id")
        return redirect("/")
    return make_response(render_template("admin/orders_panel.html", orders=data.get('data')))

@app.route("/order_detail", methods = ["GET"])
def order_detail():
    user_id = getAdminId()
    if user_id == None:
        return redirect("/")
    data = get_order_detail(user_id)
    if data.get("resualt") == False:
        session.pop("admin_id")
        return redirect("/")
    return make_response(render_template("admin/order_detail.html", data=data.get("data")))

@app.route("/chats_panel", methods = ["GET"])
def chats_admin():
    user_id = getAdminId()
    if user_id == None:
        return redirect("/")
    data = get_all_orders(user_id)
    if data.get("resualt") == False:
        session.pop("admin_id")
        return redirect("/")
    return make_response(render_template("admin/chat_admin.html"))

if __name__ == "__main__":
    app.run("0.0.0.0", port=5010)