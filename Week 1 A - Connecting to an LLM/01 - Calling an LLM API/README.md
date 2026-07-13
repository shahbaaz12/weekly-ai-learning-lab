# Calling an LLM API

## Objective

Learn how a Python program sends a prompt to an LLM and prints the answer.

## What we are building

A small terminal program that asks a model for a witty excuse for being late to the office.

## How it works

1. The program reads the Groq API settings from `.env`.
2. It creates an OpenAI client that uses Groq's OpenAI-compatible API.
3. It sends one prompt to the model and prints the returned text.

## Setup

Copy `.env.example` to `.env`, then add your Groq API key.

```env
GROQ_API_KEY=your_key_here
GROQ_API_BASE_URL=https://api.groq.com/openai/v1
```

## Run

```powershell
uv run python main.py
```

Try changing the `instructions` or `input` values in `main.py` and run it again.
