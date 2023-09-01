from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import PlainTextResponse, JSONResponse
from fastapi.encoders import jsonable_encoder
import uvicorn
import json
import aiohttp

app = FastAPI()

async def connect(websocket: WebSocket) -> bool:
    print("New client : {0}".format('ip'), flush=True)   
    await websocket.accept()
    return True

@app.get("/status")
async def status():
    print("Health market-data, OK", flush=True)
    return PlainTextResponse(content='OK\n', headers={'Content-Type' : 'text/plain'}, status_code=200)

@app.websocket("/chat")
async def websocket_endpoint(websocket: WebSocket):
    if not await connect(websocket):
        return
    try:
        while True:
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        print("Client left")

if __name__ == "__main__":
    print("Start chat", flush=True)
    uvicorn.run(app, host="0.0.0.0", port=9000)