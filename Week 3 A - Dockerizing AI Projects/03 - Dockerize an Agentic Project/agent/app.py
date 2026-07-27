# What this file does: lets an OpenAI model use calculator and clock tools, with Redis chat memory.

import json
import os

import httpx
import redis
from fastapi import FastAPI
from openai import OpenAI
from pydantic import BaseModel


app = FastAPI(title="DeskBuddy Agent")
llm = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
memory = redis.Redis(host=os.getenv("REDIS_HOST", "redis"), port=6379, decode_responses=True)
tools_url = os.getenv("TOOLS_URL", "http://tools:7000")

tool_definitions = [
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Calculate a math expression.",
            "parameters": {
                "type": "object",
                "properties": {"expression": {"type": "string"}},
                "required": ["expression"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_datetime",
            "description": "Get the current date and time.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
]


class Chat(BaseModel):
    session_id: str
    message: str


@app.get("/")
def health():
    return {"status": "DeskBuddy Agent is live"}


@app.post("/chat")
def chat(request: Chat):
    key = f"history:{request.session_id}"
    history = [json.loads(item) for item in memory.lrange(key, 0, -1)]
    messages = [{"role": "system", "content": "You are a helpful desk assistant."}]
    messages.extend(history)
    messages.append({"role": "user", "content": request.message})

    response = llm.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=tool_definitions,
    )
    message = response.choices[0].message

    if message.tool_calls:
        messages.append(message.model_dump(exclude_none=True))
        for tool_call in message.tool_calls:
            arguments = json.loads(tool_call.function.arguments)
            if tool_call.function.name == "calculator":
                result = httpx.post(f"{tools_url}/calculator", json=arguments).json()
            else:
                result = httpx.get(f"{tools_url}/datetime").json()
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result),
                }
            )

        response = llm.chat.completions.create(model="gpt-4o-mini", messages=messages)
        answer = response.choices[0].message.content
    else:
        answer = message.content

    memory.rpush(key, json.dumps({"role": "user", "content": request.message}))
    memory.rpush(key, json.dumps({"role": "assistant", "content": answer}))
    return {"answer": answer}
