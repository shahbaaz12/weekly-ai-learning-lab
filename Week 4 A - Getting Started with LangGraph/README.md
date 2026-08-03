# Week 4 A - Getting Started with LangGraph

## Objective

This week is a first look at LangGraph. The projects start with a small graph,
then add a chatbot, and finally let the chatbot use tools.

## What I built

1. **Basic Graph** - A graph with two steps that share one state.
2. **Basic Chatbot** - A Groq chat model inside a LangGraph node.
3. **Chatbot with Tools** - A chatbot that can use a local multiply tool.

## API keys

The Week 4 `.env` file uses the same `GROQ_API_KEY` from the earlier weeks, so
the chatbot projects are ready to use. If you are setting up the repository for
the first time, create `.env` from `.env.example` and add your Groq key.

## Run a project

Open this Week 4 folder in PowerShell. Each block installs that project's
packages and then runs it.

### 1. Basic Graph

```powershell
Push-Location "01 - Basic Graph"
uv sync
uv run python _1_basic_graph.py
Pop-Location
```

### 2. Basic Chatbot

```powershell
Push-Location "02 - Basic Chatbot"
uv sync
uv run python _1_basic_chatbot.py
Pop-Location
```

### 3. Chatbot with Tools

```powershell
Push-Location "03 - Chatbot with Tools"
uv sync
uv run python _1_chatbot_with_tools.py
Pop-Location
```
