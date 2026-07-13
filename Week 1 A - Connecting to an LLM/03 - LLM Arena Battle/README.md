# LLM Arena Battle

## Objective

Learn how to send the same prompt to two different models and compare their answers fairly.

## What we are building

A Gradio app that shows two anonymous answers as Model A and Model B, then lets the user vote for one.

## How it works

1. The app reads two model IDs from `.env`.
2. Both models receive exactly the same system prompt and user prompt.
3. The app displays the answers without revealing which model produced them.
4. The user can vote for the answer they prefer.

## Setup

Copy `.env.example` to `.env`, then add your Groq key, API URL, and two model names.

```env
GROQ_API_KEY=your_key_here
GROQ_API_BASE_URL=https://api.groq.com/openai/v1
GROQ_MODEL_A=openai/gpt-oss-120b
GROQ_MODEL_B=llama-3.3-70b-versatile
```

## Run

```powershell
uv run python src/app.py
```

Open the local URL, enter one prompt, and compare the two responses before voting.
