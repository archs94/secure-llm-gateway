from fastapi import FastAPI
from openai import OpenAI
from security import validate_input
import os

app = FastAPI()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


@app.post("/chat")
def chat(user_input: str):
    safe_input = validate_input(user_input)
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=safe_input
    )
    return {"response": response.output_text}
