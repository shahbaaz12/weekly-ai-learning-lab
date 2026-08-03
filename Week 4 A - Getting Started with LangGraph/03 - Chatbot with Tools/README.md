# Chatbot with Tools

## Objective

Build a chatbot that can decide when it should use the local `multiply` tool.

## Before running

The project uses `GROQ_API_KEY` from the Week 4 `.env` file.

## Run

```powershell
uv sync
uv run python _1_chatbot_with_tools.py
```

## Key idea

The first question asks for a multiplication, so the chatbot can use the local
`multiply` tool. Change the question in `_1_chatbot_with_tools.py` to try your
own calculation.

`tools_condition` checks the model response. If the model requests a tool,
LangGraph runs it and sends the result back to the model for the final answer.
