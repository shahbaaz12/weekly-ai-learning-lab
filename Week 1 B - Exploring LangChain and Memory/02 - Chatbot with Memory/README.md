# Chatbot with Memory

## Objective

Learn that an LLM remembers a conversation only when earlier messages are sent again with the new message.

## What we are building

Two terminal examples:

1. `_1_memory_demo.py` uses a fixed conversation history.
2. `_2_memory_chat.py` builds its history as you chat with the bot.

## How it works

1. `MessagesPlaceholder("history")` reserves a place for earlier conversation turns.
2. Each user message and AI response is stored as a LangChain message.
3. On the next question, the program sends the complete history with the new question.

### Why this chain has no output parser

The LangChain summarizer uses `prompt | model | parser` because it only needs plain text. This chatbot uses `prompt | model` because it needs the model's `AIMessage` structure for conversation history. We use `.content` to display the answer, while `HumanMessage` and `AIMessage` preserve who said each message.

## Setup

Copy `.env.example` to `.env`, then add your Groq API key and model name.

```env
GROQ_API_KEY=your_key_here
GROQ_MODEL=openai/gpt-oss-120b
```

## Run

First run the fixed-history example:

```powershell
uv run python src/_1_memory_demo.py
```

Then run the interactive chat:

```powershell
uv run python src/_2_memory_chat.py
```

Type `quit` to stop the chat. The memory resets when the program stops because it is stored only in the `history` list.
