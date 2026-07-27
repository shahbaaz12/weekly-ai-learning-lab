# What this file does: provides small calculator and clock tools for the agent service.

import datetime

from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI(title="DeskBuddy Tools")


class Calculation(BaseModel):
    expression: str


@app.get("/")
def health():
    return {"status": "DeskBuddy Tools is live"}


@app.post("/calculator")
def calculator(calculation: Calculation):
    return {"result": eval(calculation.expression, {"__builtins__": {}})}


@app.get("/datetime")
def now():
    return {"now": datetime.datetime.now().isoformat()}
