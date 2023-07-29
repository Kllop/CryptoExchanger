#api
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import PlainTextResponse, JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from data.direction import Direction
from data.course import Course

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

@app.get("/direction")
async def payMethods():
    return JSONResponse(content=jsonable_encoder(Direction().get_direction()))

@app.get("/course")
async def course():
    return JSONResponse(content=jsonable_encoder(Course().get_course()))
                                
@app.get("/status")
def status(request):
    pass

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9000)