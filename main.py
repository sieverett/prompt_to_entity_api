import json
import os
from typing import Optional
from uuid import uuid4
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from mangum import Mangum
from anthropic import Anthropic
from dotenv import load_dotenv
load_dotenv('.env')

client = Anthropic()


def complete_prompt_with_context(prompt, template):
    with open(template, 'r') as f:
        prompt_text = f.read()
    complete_prompt = prompt_text.replace('{context}', prompt)
    return complete_prompt


def call_llm(user_message):
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        messages=[
            {"role": "user", "content": user_message}
        ]
    )
    return response.content[0].text


class Prompt(BaseModel):
    message: str
    prompt_id: Optional[str] = uuid4().hex


app = FastAPI()
handler = Mangum(app)


@app.get("/")
async def root():
    return {"message": "Welcome to Flow.AI's prompt to object parser API"}

@app.post("/get-objects")
async def parse_message(prompt: Prompt):
    prompt.prompt_id = uuid4().hex
    try:
        prompt2 = call_llm(complete_prompt_with_context(prompt.message, 'prompt_template_1.txt'))
        response = call_llm(complete_prompt_with_context(prompt2, 'prompt_template_2.txt'))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM call failed: {e}")

    return {"response": response}
