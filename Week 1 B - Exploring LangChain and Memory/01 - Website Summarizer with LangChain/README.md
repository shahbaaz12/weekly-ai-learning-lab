# Website Summarizer with LangChain

## Objective

Learn how LangChain turns a prompt, a model, and an output parser into one reusable pipeline.

## What we are building

A terminal website summarizer that fetches a page and returns a short Markdown summary.

## How it works

1. The scraper fetches the website and removes noisy page elements.
2. `ChatPromptTemplate` creates the reusable instructions and fills in the website text.
3. `ChatGroq` sends the completed prompt to the Groq model.
4. `StrOutputParser` turns the model response into plain text.

The important LangChain line is:

```python
chain = prompt | model | parser
```

This project deliberately reuses the scraper idea from Week 1 A. The new learning goal is the LangChain pipeline.

## Setup

Copy `.env.example` to `.env`, then add your Groq API key and model name.

```env
GROQ_API_KEY=your_key_here
GROQ_MODEL=openai/gpt-oss-120b
```

## Run

```powershell
uv run python src/summarizer_langchain.py
```

Enter a public website URL when the program asks for one.
