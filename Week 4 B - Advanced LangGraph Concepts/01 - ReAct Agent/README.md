# ReAct Agent

## Objective

Build a graph where the model can use a tool before giving its final answer.

## Before running

This project uses `GROQ_API_KEY` from the Week 4 B `.env` file.

## Run

```powershell
uv sync
uv run python _1_react_agent.py
```

## Key idea

ReAct means the model can reason about what to do, use a tool when it needs one,
and then answer using the tool result. Here, it chooses the local `multiply`
tool to answer a calculation.
