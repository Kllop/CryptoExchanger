#api
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import PlainTextResponse, JSONResponse
from fastapi.encoders import jsonable_encoder
import uvicorn

from data.direction import Direction

#folders
from market_course import MarketCouse

app = FastAPI()
marketCourse = MarketCouse()

@app.get("/direction")
def payMethods():
    return JSONResponse(content=jsonable_encoder(Direction().get_direction()))

@app.websocket("/course")
def course(request):
    pass
                                
@app.get("/status")
def status(request):
    pass

@app.get("/courseHTML")
def courseHTML(request):
    return marketCourse.getData()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9000)