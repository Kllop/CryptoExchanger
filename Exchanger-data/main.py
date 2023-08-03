#api
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import PlainTextResponse, JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from data.direction import Direction
from data.course import Course
from data.orders import Orders

#folders
from market_course import MarketCouse

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
Orders().RemoveTable()

@app.get("/direction")
async def payMethods(request: Request):
    return JSONResponse(content=jsonable_encoder(Direction().get_direction()))

@app.get("/course")
async def course(request: Request):
    return JSONResponse(content=jsonable_encoder(Course().get_course()))
                                
@app.get("/status")
def status(request: Request):
    pass

@app.post("/bid")
async def status(request: Request):
    jsdata = await request.json()
    print(jsdata, flush=True)
    Orders().send_order(jsdata)
    return JSONResponse(content=jsonable_encoder(jsdata))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9000)