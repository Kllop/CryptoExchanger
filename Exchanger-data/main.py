#api
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, Response
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

#folders
from data.direction import Direction
from data.course import Course
from data.orders import Orders
from data.registraton_user import Registraton
from data.login_user import Login
from data.sender_mail import Sender_Email
from data.telegram_message import TelegramMessage

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

seneder_email = Sender_Email()
telegram_message = TelegramMessage()


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

    #payment or cancel#
@app.post("/status")
async def status(request: Request):
    jsdata = await request.json()
    resualt = Orders().change_status_order(jsdata.get("key"), jsdata.get("status"))
    if jsdata.get("status") == "payment":
        order_data = Orders().getOrder(jsdata.get("key")).get("data")
        telegram_message.sendOrderInfo(order_data)
    elif jsdata.get("status") == "cancel":
        telegram_message.sendCencelOder()
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
    data, course, count = Orders().send_order(jsdata)
    telegram_message.sendNewOrder()
    try:
        seneder_email.send_order_email(jsdata.get("setter_email"), jsdata.get('setterType'), jsdata.get('getterType'), course, count, jsdata.get('getterType'), jsdata.get('getterNumber'))
    except Exception as e:
        print(e, flush=True)
    return JSONResponse(content=jsonable_encoder(data))

@app.post("/order")
async def order(request: Request):
    jsdata = await request.json()
    data = Orders().getOrder(jsdata['order_id'])
    return JSONResponse(content=jsonable_encoder(data))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9000)