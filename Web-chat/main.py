from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import PlainTextResponse, JSONResponse
from fastapi.encoders import jsonable_encoder
import uvicorn
import uuid
import json

app = FastAPI()
chats = {}
connection = {}

async def connect(websocket: WebSocket) -> bool:
    print("New client chat : {0}".format('ip'), flush=True)   
    await websocket.accept()
    uid_chat = uuid.uuid4().hex
    uid_chat = "1234"
    chats.update({uid_chat : {"new_message" : False, "messages" : []}})
    connection.update({uid_chat : websocket})
    websocket.cookies.update({"uuid" : uid_chat})
    return True

async def connect_admin(websocket: WebSocket) -> bool:
    await websocket.accept()
    return True

async def get_messages(uid:str) -> bool:
    return chats.get(uid)

async def send_message_server(uid:str) -> bool:
    return chats.get(uid)

async def send_message_clien(uid:str, message:str) -> None:
    websocket = connection.get(uid)
    await websocket.send_text(message)

async def send_message_clien_ws(message:str) -> None:
    jsdata = json.loads(message)
    await send_message_clien(jsdata.get("uuid"), jsdata.get("message"))

async def set_new_message(websocket: WebSocket, new_message:str) -> None: 
    uid = websocket.cookies.get("uuid")
    data = await get_messages(uid)
    if data == None:
        await websocket.close(414)
    data['new_message'] = True
    data['messages'].append(new_message)
    chats.update({uid : data})

@app.get("/status")
async def status():
    print("Health market-data, OK", flush=True)
    return PlainTextResponse(content='OK\n', headers={'Content-Type' : 'text/plain'}, status_code=200)

@app.post("/send_message")
async def send_message(request: Request):
    jsdata = await request.json()
    uid = jsdata.get("uuid")
    message = jsdata.get("message")
    await send_message_clien(uid, message)
    return PlainTextResponse(content='OK\n', headers={'Content-Type' : 'text/plain'}, status_code=200)

@app.websocket("/chat")
async def websocket_endpoint_client(websocket: WebSocket):
    if not await connect(websocket):
        return
    try:
        while True:
            data = await websocket.receive_text()
            await set_new_message(websocket, data)
    except WebSocketDisconnect:
        print("Client left")

@app.websocket("/admin_chat")
async def websocket_endpoint_admin(websocket: WebSocket):
    if not await connect_admin(websocket):
        return
    try:
        while True:
            data = await websocket.receive_text()
            await send_message_clien_ws(data)
    except WebSocketDisconnect:
        print("Client left")

if __name__ == "__main__":
    print("Start chat", flush=True)
    uvicorn.run(app, host="0.0.0.0", port=9000)