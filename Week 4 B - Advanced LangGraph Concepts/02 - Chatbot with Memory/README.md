# Chatbot with Memory

## Objective

Build a chatbot that remembers earlier messages in the same conversation.

## Before running

This project uses `GROQ_API_KEY` from the Week 4 B `.env` file.

## Run

```powershell
uv sync
uv run python _1_chatbot_with_memory.py
```

## Key idea

`MemorySaver` stores the state for a `thread_id`. Because both questions use
the same thread, the second question can use information from the first one.
