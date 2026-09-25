from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Hotel Chatbot API")

from services.db import connect_to_mongo, close_mongo_connection

@app.on_event("startup")
async def startup_db_client():
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_db_client():
    await close_mongo_connection()

# Allow requests from the frontend widget
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this to the widget's domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Hotel Chatbot API"}

from pydantic import BaseModel
from typing import List

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]

from services.chat import generate_chat_response

@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    messages_dict = [{"role": msg.role, "content": msg.content} for msg in request.messages]
    reply = await generate_chat_response(messages_dict)
    return {"reply": reply}
