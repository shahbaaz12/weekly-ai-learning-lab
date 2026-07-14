# Tool-Using Shop Assistant

## Objective

Learn how an LLM can decide to call a normal Python function when it needs information.

## What we are building

A Gradio shop chatbot that answers price questions about shoes, hats, bags, shorts, and pants.

## How it works

1. The model receives the user's message and a description of the `get_price` tool.
2. For a price question, the model asks Python to call that tool.
3. The tool in `shop_database.py` reads the item price from the `PRICES` dictionary.
4. Python sends the tool result back to the model so it can write a friendly answer.

`agent.py` manages the AI and tool-call flow. `shop_database.py` keeps the local price data and lookup function separate.

## Understanding `messages` and tool calls

`messages` is a normal Python list that holds the conversation needed to answer one question. For `How much are the shoes?`, it grows like this:

```text
System: You are a shop assistant.
User: How much are the shoes?
Assistant: I want to call get_price("shoes").
Tool: The price of shoes is ₹799.
```

The model does not run your Python function. It only asks to use `get_price`. Your program runs the function locally, then sends its result back to the model.

`message` means the latest response from the model. `messages` means the complete list of conversation messages.

Unlike `_2_memory_chat.py`, this list is created again for every new question. The shop assistant can use the tool during one answer, but it does not remember earlier chats yet.

## Setup

Copy `.env.example` to `.env`, then add your Groq API key and model name.

```env
GROQ_API_KEY=your_key_here
GROQ_MODEL=openai/gpt-oss-120b
```

## Run

Start the browser chatbot:

```powershell
uv run python src/app.py
```

Open the local URL printed in the terminal and ask: `How much are the pants?`

You can also test the tool flow directly:

```powershell
uv run python src/agent.py
```
