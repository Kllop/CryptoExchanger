#api
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, Response
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import uuid
import hashlib

#Folder
from data.preference import DirectionPreference
from data.orders import OrderInfo

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

login = "MisPIcudesTormAToCLo"
password = "27865PHhuYxkk2EdaUYR"
user_id = uuid.uuid4().hex
direction = DirectionPreference()
order_info = OrderInfo()

@app.post("/admin_login")
async def login_admin(request: Request):
    jsdata = await request.json()
    if login == jsdata.get("login") and password == jsdata.get("password"):
        uid_chat = "123"
        return JSONResponse(content=jsonable_encoder({"resualt" : True, "id" : user_id, "uuid" : uid_chat}))
    return JSONResponse(content=jsonable_encoder({"resualt" : False, "id" : "", "uuid" : ""}))

@app.post("/admin_chat")
async def all_orders(request: Request):
    jsdata = await request.json()
    uid = jsdata.get("uuid") == user_id
    resualt = hashlib.sha256(user_id) == uid
    return JSONResponse(content=jsonable_encoder({"resualt" : resualt}))

######################## DIRECTION ##############################

@app.post("/all_direction")
async def all_orders(request: Request):
    jsdata = await request.json()
    if jsdata.get("id") == user_id:
        return JSONResponse(content=jsonable_encoder({"resualt" : True, "data" : direction.getAllDirection()}))
    return JSONResponse(content=jsonable_encoder({"resualt" : False, "data" : []}))

@app.post("/remove_direction")
async def order_detail(request: Request):
    jsdata = await request.json()
    if jsdata.get("id") == user_id:
        direction.removeDirection(jsdata.get("uid"))
        return JSONResponse(content=jsonable_encoder({"resualt" : True, "data" : []}))
    return JSONResponse(content=jsonable_encoder({"resualt" : False, "data" : []}))

@app.post("/create_direction")
async def order_detail(request: Request):
    jsdata = await request.json()
    if jsdata.get("id") == user_id:
        coin = jsdata.get("coin")  
        pay_method = jsdata.get("pay_method")
        bank_ru = jsdata.get("bank_ru")
        bank_en = jsdata.get("bank_en")
        bank_ind = jsdata.get("bank_ind")
        percent = jsdata.get("percent")
        area = jsdata.get("area").lower()
        market = jsdata.get("market").lower()
        direction.createDirection(coin, pay_method, bank_ru, bank_en, bank_ind, percent, area, market)
        return JSONResponse(content=jsonable_encoder({"resualt" : True, "data" : []}))
    return JSONResponse(content=jsonable_encoder({"resualt" : False, "data" : []}))

######################## ORDERS ##############################

@app.post("/all_orders")
async def all_orders(request: Request):
    jsdata = await request.json()
    if jsdata.get("id") == user_id:
        return JSONResponse(content=jsonable_encoder({"resualt" : True, "data" : order_info.GetAllOrders()}))
    return JSONResponse(content=jsonable_encoder({"resualt" : False, "data" : []}))

@app.post("/order_detail")
async def order_detail(request: Request):
    jsdata = await request.json()
    if jsdata.get("id") == user_id:
        order_id = jsdata.get("order_id")
        return JSONResponse(content=jsonable_encoder({"resualt" : True, "data" : order_info.GetOrderDetail(int(order_id))}))
    return JSONResponse(content=jsonable_encoder({"resualt" : False, "data" : []}))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9010)