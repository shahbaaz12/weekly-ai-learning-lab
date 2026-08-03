# Basic Chatbot

## Objective

Use one LangGraph node to send a message to Groq and return the AI response.

## Before running

This project uses `GROQ_API_KEY` from the Week 4 `.env` file. It is the same
key used in the earlier Groq projects.

## Run

```powershell
uv sync
uv run python _1_basic_chatbot.py
```

## Key idea

The `chatbot` node reads the current `messages`, calls the model, and adds the
answer back to the graph state. This is the basic pattern behind a chatbot graph.
