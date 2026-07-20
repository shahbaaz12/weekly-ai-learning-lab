# Working with Agents

## Objective

Learn how a LangChain agent manages the tool-calling loop automatically: it decides which tool to call, runs the tool, sends the result back to the model, and returns a final answer.

## Scripts

| Script | What it demonstrates |
|---|---|
| `_1_basic_agent.py` | An inventory agent with one stock-checking tool. |
| `_2_agent_with_multiple_tools.py` | An inventory agent with stock and price tools, plus printing the message sequence returned by the agent. |

## Run

Run these commands from this folder:

```powershell
uv sync
uv run python _1_basic_agent.py
uv run python _2_agent_with_multiple_tools.py
```

## Key idea

Unlike the manual tool-call examples in Project 1, these scripts do not need to inspect `tool_calls`, execute the tool, or append tool messages themselves. `create_agent()` performs that work.

This project uses Groq and requires `GROQ_API_KEY` in the repository-root `.env` file.
