from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()
from app.routes.test import send_chat_msg
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")

# client = OpenAI()
# thread = client.beta.threads.create()

router = APIRouter()

# Replace this with your OpenAI API key
# openai.api_key = "YOUR_OPENAI_API_KEY"

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

@router.post("/", response_model=ChatResponse)
def chat_with_ai(request: ChatRequest):
    try:
        import time
        time.sleep(1)

        response = send_chat_msg(request.message)

        # response = openai.Completion.create(
        #     engine="text-davinci-003",
        #     prompt=request.message,
        #     max_tokens=150,
        # )
        # return {"response": response.choices[0].text.strip()}
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
