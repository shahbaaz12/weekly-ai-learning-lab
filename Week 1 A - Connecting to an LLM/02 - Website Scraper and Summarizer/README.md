# Website Scraper and Summarizer

## Objective

Learn how to collect text from a website and use an LLM to create a useful summary.

## What we are building

A small Gradio web app where a user enters a public website URL and receives an AI-generated Markdown summary.

## How it works

1. The Gradio interface accepts a website URL.
2. The scraper downloads the page, removes noisy HTML elements, and keeps the readable text.
3. The summarizer sends that text to Groq with instructions for a clear summary.
4. The result appears in the browser.

## Setup

Copy `.env.example` to `.env`, then add your Groq API key and model name.

```env
GROQ_API_KEY=your_key_here
GROQ_API_BASE_URL=https://api.groq.com/openai/v1
GROQ_MODEL=openai/gpt-oss-120b
```

## Run

```powershell
uv run python src/app.py
```

Open the local URL printed in the terminal and try a public website such as `https://www.python.org/`.
