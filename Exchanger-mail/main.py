#api
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, Response
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import uuid
import hashlib

#FOLDERS
from data.sender_mail import Sender_Email


app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
sender_mail = Sender_Email()

@app.post("/send_order_info")
async def login_admin(request: Request):
    sender_mail.send_order_email()
    return JSONResponse(content=jsonable_encoder({"resualt" : True}))



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9010)