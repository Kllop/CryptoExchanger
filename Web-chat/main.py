from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import PlainTextResponse
from datetime import datetime
import aiohttp
import uvicorn
import uuid
import json

app = FastAPI()

class TelegramMessage:
    
    def __init__(self) -> None:
        self.TeleBot = '6163052051:AAHpUAmWaU9Vlf71kyAZ-brg2fet_CUvx0E'
        self.chatID = '5829831042'

    async def sendAsyncMessage(self, message:str) -> None:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.telegram.org/bot{0}/sendMessage?chat_id={1}&text={2}".format(self.TeleBot, self.chatID, message)) as resp:
                print(resp.status, flush=True)


class ChatsData:
    chats = {}

    async def __getTime__(self):
        return datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    async def __getChatData__(self, uid:str) -> dict:
        return self.chats.get(uid)
    
    async def __createChat__(self, uid) -> dict:
        return  {"new_message" : False, "messages" : [], "uuid_chat" : uid}
    
    async def get_all_chats_data(self) -> dict:
        return self.chats
    
    async def get_all_messages(self, uid:str) -> dict:
        out_data = self.chats.get(uid)
        if out_data == None:
            return {}
        return out_data
    
    async def create_new_chat(self, uid:str) -> None:
        data = await self.__getChatData__(uid)
        if data == None:
            self.chats.update({uid : await self.__createChat__(uid)})
        
    async def set_new_message(self, uid:str, new_message:str, isNewMessage:bool, owner:str) -> str: 
        data = await self.__getChatData__(uid)
        if data == None:
            data = await self.__createChat__(uid)
        date = await self.__getTime__()
        data['new_message'] = isNewMessage
        data['messages'].append({"date" : date, "message" : new_message, "owner" : owner})
        self.chats.update({uid : data})

class Connection:

    admin_connection = {}
    client_connection = {}
    chats_data = ChatsData()
    telegramMessage = TelegramMessage()

    async def __send_message_client__(self, uid:str) -> None:
        websocket = self.client_connection.get(uid)
        if websocket == None:
            return
        await websocket.send_json(await self.chats_data.get_all_messages(uid))

    async def __send_message_admin__(self) -> None:
        for websocket in self.admin_connection.values():
            await websocket.send_json(await self.chats_data.get_all_chats_data())

    async def set_message_client(self, uid:str, message:str) -> None:
        await self.chats_data.set_new_message(uid, message, True, "Client")
        await self.__send_message_admin__()
        await self.__send_message_client__(uid)
        await self.telegramMessage.sendAsyncMessage("У вас новое сообщение в чате")

    async def set_message_admin(self, data:str) -> None:
        jsdata = json.loads(data)
        uid = jsdata.get("uuid")
        message = jsdata.get("message")
        await self.chats_data.set_new_message(uid, message, False, "Operator")
        await self.__send_message_client__(uid)
        await self.__send_message_admin__()

    async def set_connection_client(self, websocket: WebSocket) -> None:
        await websocket.accept()
        uid_chat = websocket.cookies.get("uuid_chat")
        data = await self.chats_data.get_all_messages(uid_chat)
        if uid_chat == None or len(data) == 0:
            uid_chat = uuid.uuid4().hex
        print("Open new client chat : ip - {0}, uuid - {1}".format('ip', uid_chat), flush=True)   
        self.client_connection.update({uid_chat : websocket})
        websocket.cookies.update({"uuid" : uid_chat})
        await self.__send_message_client__(uid_chat)
        return True

    async def set_connection_admin(self, websocket: WebSocket) -> None:
        await websocket.accept()
        uid_chat = uuid.uuid4().hex
        print("Open new admin chat : ip - {0}, uuid - {1}".format('ip', uid_chat), flush=True)   
        self.admin_connection.update({uid_chat : websocket})
        websocket.cookies.update({"uuid" : uid_chat})
        await self.__send_message_admin__()
        return True

    async def close_connection_client(self, uid:str) -> None:
        self.client_connection.pop(uid)

    async def close_connection_admin(self, uid:str) -> None:
        self.admin_connection.pop(uid)

connection = Connection()

@app.get("/status")
async def status():
    print("Health market-data, OK", flush=True)
    return PlainTextResponse(content='OK\n', headers={'Content-Type' : 'text/plain'}, status_code=200)

@app.websocket("/chat")
async def websocket_endpoint_client(websocket: WebSocket):
    if not await connection.set_connection_client(websocket):
        return
    try:
        while True:
            data = await websocket.receive_text()
            uid = websocket.cookies.get("uuid")
            await connection.set_message_client(uid, data)
    except WebSocketDisconnect:
        uid = websocket.cookies.get("uuid")
        await connection.close_connection_client(uid)
        print("Client close chat")

@app.websocket("/admin_chat")
async def websocket_endpoint_admin(websocket: WebSocket):
    if not await connection.set_connection_admin(websocket):
        return
    try:
        while True:
            data = await websocket.receive_text()
            await connection.set_message_admin(data)
    except WebSocketDisconnect:
        uid = websocket.cookies.get("uuid")
        await connection.close_connection_admin(uid)
        print("Admin close chat")

if __name__ == "__main__":
    print("Start chat", flush=True)
    uvicorn.run(app, host="0.0.0.0", port=9020)