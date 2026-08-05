# Week 4 B - Advanced LangGraph Concepts

## Objective

Continue the LangGraph journey by learning how an AI can use tools, remember a
conversation, stream graph updates, and pause for a human decision.

## What I built

1. **ReAct Agent** - A chatbot that decides when to use a local tool.
2. **Chatbot with Memory** - A chatbot that remembers information in the same conversation.
3. **Streaming Chatbot** - A chatbot that shows each graph update as it happens.
4. **Human in the Loop** - A graph that pauses for a human answer before it continues.

## API key

Projects 1, 2, and 3 use the same `GROQ_API_KEY` from the earlier weeks. If you
are setting up the repository for the first time, create `.env` from
`.env.example` and add your Groq key.

Project 4 runs locally and does not need an API key.

## Run a project

Open this Week 4 B folder in PowerShell. Each block installs that project's
packages and then runs it.

### 1. ReAct Agent

```powershell
Push-Location "01 - ReAct Agent"
uv sync
uv run python _1_react_agent.py
Pop-Location
```

### 2. Chatbot with Memory

```powershell
Push-Location "02 - Chatbot with Memory"
uv sync
uv run python _1_chatbot_with_memory.py
Pop-Location
```

### 3. Streaming Chatbot

```powershell
Push-Location "03 - Streaming Chatbot"
uv sync
uv run python _1_streaming_chatbot.py
Pop-Location
```

### 4. Human in the Loop

```powershell
Push-Location "04 - Human in the Loop"
uv sync
uv run python _1_human_in_the_loop.py
Pop-Location
```
