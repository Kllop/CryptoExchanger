#api
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, Response
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import uuid
import json
import hashlib

#Folder
from Database import Redis_DB
from Database import Postgres_DB

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

redis_db = Redis_DB()
postgres_db = Postgres_DB("ownerdb", "X$Oi815H%nd*FLyB!9v%", "postgres-data", "5432", "exchange")

login = "MisPIcudesTormAToCLo"
password = "27865PHhuYxkk2EdaUYR"
user_id = uuid.uuid4().hex

@app.post("/admin_login")
async def login_admin(request: Request):
    jsdata = await request.json()
    if login == jsdata.get("login") and password == jsdata.get("password"):
        uid_chat = "123"
        return JSONResponse(content=jsonable_encoder({"resualt" : True, "id" : user_id, "uuid" : uid_chat}))
    return JSONResponse(content=jsonable_encoder({"resualt" : False, "id" : "", "uuid" : ""}))

@app.post("/all_orders")
async def all_orders(request: Request):
    jsdata = await request.json()
    if jsdata.get("id") == user_id:
        return JSONResponse(content=jsonable_encoder({"resualt" : True, "data" : postgres_db.GetAllOrders()}))
    return JSONResponse(content=jsonable_encoder({"resualt" : False, "data" : []}))

@app.post("/admin_chat")
async def all_orders(request: Request):
    jsdata = await request.json()
    uid = jsdata.get("uuid") == user_id
    resualt = hashlib.sha256(user_id) == uid
    return JSONResponse(content=jsonable_encoder({"resualt" : resualt}))

@app.post("/order_detail")
async def order_detail(request: Request):
    jsdata = await request.json()
    if jsdata.get("id") == user_id:
        order_id = jsdata.get("order_id")
        return JSONResponse(content=jsonable_encoder({"resualt" : True, "data" : postgres_db.GetOrderDetail(int(order_id))}))
    return JSONResponse(content=jsonable_encoder({"resualt" : False, "data" : []}))

def createDirection():
    #postgres_db.DropTable("DirectionPreference")
    postgres_db.ClearTable("DirectionPreference")
    
    postgres_db.SendDirectoion("BTC", "64", "Райффайзен RUB", "Raiffeisen RUB", "Raiffeisen", 5.00, "P2P")
    postgres_db.SendDirectoion("ETH", "64", "Райффайзен RUB", "Raiffeisen RUB", "Raiffeisen", 5.00, "P2P")
    postgres_db.SendDirectoion("USDT", "64", "Райффайзен RUB", "Raiffeisen RUB", "Raiffeisen", 5.00, "P2P")

    postgres_db.SendDirectoion("BTC", "64", "Сбербанк RUB", "Sberbank RUB", "Sberbank", 5.00, "P2P")
    postgres_db.SendDirectoion("ETH", "64", "Сбербанк RUB", "Sberbank RUB", "Sberbank", 5.00, "P2P")
    postgres_db.SendDirectoion("USDT", "64", "Сбербанк RUB", "Sberbank RUB", "Sberbank", 5.00, "P2P")

    #postgres_db.SendDirectoion("BTC", "64", "Альфабанк RUB", "Alfabank RUB", "Alfabank", 5.00, "P2P")
    #postgres_db.SendDirectoion("ETH", "64", "Альфабанк RUB", "Alfabank RUB", "Alfabank", 5.00, "P2P")
    #postgres_db.SendDirectoion("USDT", "64", "Альфабанк RUB", "Alfabank RUB", "Alfabank", 5.00, "P2P")

    postgres_db.SendDirectoion("BTC", "64", "Тинькофф RUB", "Tinkoff RUB", "Tinkoff", 5.00, "P2P")
    postgres_db.SendDirectoion("ETH", "64", "Тинькофф RUB", "Tinkoff RUB", "Tinkoff", 5.00, "P2P")
    postgres_db.SendDirectoion("USDT", "64", "Тинькофф RUB", "Tinkoff RUB", "Tinkoff", 5.00, "P2P")

def setReidsDirection():
    postgre_data = postgres_db.GetDirection()
    redis_db.removeKey("tradepreference")
    for data in postgre_data:
        send_data = {"coin" : data[0], "name_exch" : data[1], "name_ru" : data[2], "name_en" : data[3], "name_des" : data[4], "percent" : data [5], "market" : data[6]}
        redis_db.setValueList("tradepreference", json.dumps(send_data))

if __name__ == "__main__":
    createDirection()
    setReidsDirection()
    uvicorn.run(app, host="0.0.0.0", port=9010)