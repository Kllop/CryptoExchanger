#api
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import PlainTextResponse, JSONResponse
from fastapi.encoders import jsonable_encoder
import uvicorn

#folders
from market_course import MarketCouse

app = FastAPI(__name__)
marketCourse = MarketCouse()

@app.get("/pay_methods")
def payMethods(request):
    pass

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