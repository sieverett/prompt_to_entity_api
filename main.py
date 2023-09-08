import json
import os
from typing import Literal, Optional
from uuid import uuid4
from fastapi import FastAPI, HTTPException
import random
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from mangum import Mangum
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
# load_dotenv(os.path.join(os.path.dirname('.'), '.env'))

class Prompt(BaseModel):
    message: str
    prompt_id: Optional[str] = uuid4().hex


app = FastAPI()
handler = Mangum(app)


prompt_text = """
Follow these steps: 
\nMake a spatially consistent scene description for "{context}"
\nSimplify the scene description
\nExtract the main entities
\Make a valid JSON array with the following:
  \n- Give back the spatial coordinates to place them in the scene
  \n- Give back the scale of the entities consistently
  \n- Do not generate more that 4 entities
  \n- Include any natural entities, such as roads, rivers, mountains, volcanoes, canyons, etc.
  \n- Return the response as a valid JSON array
  


\nUse this JSON format of an airplane with spatial coordinates and scale as an example to place in a scene:

\nReturn the Output and no other items in your response

\nOutput:

{
  "assets": [
    {
      "title": "airplane",
      "position": "{“x”: 5, “y”: 3, “z”: 1}",
      "scale":  "{“length”: 20, “width”: 2, “height”: 10}"
      }
  ]
}

"""

@app.get("/")
async def root():
    return {"message": "Welcome to Flow.AI's prompt to object parser API"}

@app.post("/get-objects")
async def parse_message(prompt: Prompt):
    prompt.prompt_id = uuid4().hex
    try:
        llm = OpenAI(openai_api_key='OPENAI_API_KEY here')
    except:
        print('unable to authenticate with openai')
    prompt_1 = prompt_text.replace('{context}',prompt.message)


    print(prompt_1)
    response = llm.predict(prompt_1)
    print(response)
    try:
        response=response.split("Output:")[1].replace("\n",'')
    except:
        response=response
    
    print('returned:', response)

    return {"response":response}
