#api
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import PlainTextResponse, JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import requests

#folders
from market_course import MarketCouse

from data.direction import Direction
from data.course import Course
from data.orders import Orders

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

class TelegramMessage:
    
    def __init__(self) -> None:
        self.TeleBot = '6163052051:AAHpUAmWaU9Vlf71kyAZ-brg2fet_CUvx0E'
        self.chatID = '5829831042'
    
    def sendMessage(self, message:str):   
        requests.get("https://api.telegram.org/bot{0}/sendMessage?chat_id={1}&text={2}".format(self.TeleBot, self.chatID, message))

@app.get("/direction")
async def payMethods(request: Request):
    return JSONResponse(content=jsonable_encoder(Direction().get_direction()))

@app.get("/course")
async def course(request: Request):
    return JSONResponse(content=jsonable_encoder(Course().get_course()))
                                
@app.get("/status")
def status(request: Request):
    pass


##########  LOCAL  #############
#       payment or cancel      #
@app.post("/status")
async def status(request: Request):
    jsdata = await request.json()
    resualt = Orders().change_status_order(jsdata.get("key"), jsdata.get("status"))
    if jsdata.get("status") == "payment":
        order_data = Orders().getOrder(jsdata.get("key")).get("data")
        TelegramMessage().sendMessage("""Покупатель оплатил ордер № {0} на сумму {1} RUB, переведите {2} в 
                                      количестве {3} на адрес {4}""".format(order_data.get("orderID"), order_data.get("price"), 
                                                                            order_data.get("coin"), order_data.get("count"),
                                                                            order_data.get("wallet")))
    elif jsdata.get("status") == "cancel":
        TelegramMessage().sendMessage("Ордер был отменен")
    return JSONResponse(content=jsonable_encoder({"resualt" : resualt, "message" : ""}))

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