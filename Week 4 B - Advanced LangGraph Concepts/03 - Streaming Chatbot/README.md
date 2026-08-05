# Streaming Chatbot

## Objective

See the update produced by a chatbot node as the graph runs.

## Before running

This project uses `GROQ_API_KEY` from the Week 4 B `.env` file.

## Run

```powershell
uv sync
uv run python _1_streaming_chatbot.py
```

## Key idea

Instead of waiting for `invoke` to return the final graph state, `stream`
returns updates as nodes finish. The two questions use the same thread, so the
second reply can remember the first message.
