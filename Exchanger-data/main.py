#api
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, Response
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import requests

#folders
from market_course import MarketCouse

from data.direction import Direction
from data.course import Course
from data.orders import Orders
from data.registraton_user import Registraton
from data.login_user import Login

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

marketCourse = MarketCouse()
#Registraton().db.DropTable("UsersData")
#Registraton().db.DropTable("OrdersList")
#Registraton().send_registraton_admin('admin', '100699', 'admin@gmail.com', '127.0.0.1','')

class TelegramMessage:
    
    def __init__(self) -> None:
        self.TeleBot = '6163052051:AAHpUAmWaU9Vlf71kyAZ-brg2fet_CUvx0E'
        self.chatID = '5829831042'
    
    def sendMessage(self, message:str):   
        requests.get("https://api.telegram.org/bot{0}/sendMessage?chat_id={1}&text={2}".format(self.TeleBot, self.chatID, message))

##########  LOCAL  #############
@app.get("/request-exportxml.xml")
async def request_exportxml(request: Request):
    return Response(content=Course().get_course_xml(), media_type="application/xml")

@app.get("/direction")
async def payMethods(request: Request):
    return JSONResponse(content=jsonable_encoder(Direction().get_direction()))

@app.get("/course")
async def course(request: Request):
    return JSONResponse(content=jsonable_encoder(Course().get_course()))

#       payment or cancel      #
@app.post("/status")
async def status(request: Request):
    jsdata = await request.json()
    resualt = Orders().change_status_order(jsdata.get("key"), jsdata.get("status"))
    if jsdata.get("status") == "payment":
        order_data = Orders().getOrder(jsdata.get("key")).get("data")
        TelegramMessage().sendMessage("""Покупатель оплатил ордер № {0} {1} на сумму {2} RUB, переведите {3} в количестве {4} на адрес {5} **********************\ntelegram : {6}, курс {7}""".format(
            order_data.get("orderID"), order_data.get("pay_type"), order_data.get("price"), order_data.get("coin"), order_data.get("count"), 
            order_data.get("wallet"), order_data.get("telegram"), order_data.get("course")))
    elif jsdata.get("status") == "cancel":
        TelegramMessage().sendMessage("Ордер был отменен")
    return JSONResponse(content=jsonable_encoder({"resualt" : resualt, "message" : ""}))

@app.post("/registration")
async def registration(request: Request):
    data = await request.json()
    login = data.get("login")
    password = data.get("password")
    ip = data.get("ip")
    email = data.get("email")
    if login == None or password == None or ip == None or email == None:
        print("Error not attribute login, password, ip", flush=True)
        return JSONResponse(content=jsonable_encoder({'resualt' : False, "message" : "Registraton error, has not attribute"}))
    outdata = Registraton().send_registraton_user(data.get("login"), data.get("password"), data.get("email"), data.get("ip"), data.get("referal"))
    print(outdata, flush=True)
    return JSONResponse(content=jsonable_encoder(outdata))

@app.post("/referalcode")
async def referal(request: Request):
    data = await request.json()
    code_id = data.get("id")
    if code_id == None:
        return {"resualt" : False, "referal" : ""}
    outdata = Login().referal_code(code_id)
    return JSONResponse(content=jsonable_encoder(outdata))

@app.post("/countreferal")
async def referal(request: Request):
    data = await request.json()
    code_id = data.get("id")
    if code_id == None:
        return {"resualt" : False, "count" : 0}
    outdata = Login().referal_count(code_id)
    return JSONResponse(content=jsonable_encoder(outdata))

@app.post("/allmybids")
async def referal(request: Request):
    data = await request.json()
    code_id = data.get("id")
    if code_id == None:
        return {"resualt" : False, "data" : []}
    outdata = Orders().getAllMyBids(code_id)
    return JSONResponse(content=jsonable_encoder(outdata))

@app.post("/referalbid")
async def referal(request: Request):
    data = await request.json()
    code_id = data.get("id")
    if code_id == None:
        return {"resualt" : False, "data" : []}
    outdata = Login().referal_bid(code_id)
    return JSONResponse(content=jsonable_encoder(outdata)) 

@app.post("/authorization")
async def authorization(request: Request):
    data = await request.json()
    login = data.get("login")
    password = data.get("password")
    ip = data.get("ip")
    if login == None or password == None or ip == None:
        print("Error not attribute login, password, ip", flush=True)
        return JSONResponse(content=jsonable_encoder({"resualt" : False, "id" : ""}))
    outdata = Login().send_login(login, password, ip)
    print(outdata, flush=True)
    return JSONResponse(content=jsonable_encoder(outdata))

@app.post("/bid")
async def status(request: Request):
    jsdata = await request.json()
    data = Orders().send_order(jsdata)
    TelegramMessage().sendMessage("У вас новая заявка")
    return JSONResponse(content=jsonable_encoder(data))

@app.post("/order")
async def order(request: Request):
    jsdata = await request.json()
    data = Orders().getOrder(jsdata['order_id'])
    return JSONResponse(content=jsonable_encoder(data))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9000)