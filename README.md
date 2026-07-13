# Weekly AI Learning Lab

## Objective

Build AI projects week by week and learn each concept by using it in working code.

 

## Repository structure

```text
Weekly AI Learning Lab/
├── Week 1 A - Connecting to an LLM/
│   ├── 01 - Calling an LLM API/
│   ├── 02 - Website Scraper and Summarizer/
│   └── 03 - LLM Arena Battle/
└── Week 1 B - Exploring LangChain and Memory/
    ├── 01 - Website Summarizer with LangChain/
    ├── 02 - Chatbot with Memory/
    └── 03 - Tool-Using Shop Assistant/
```

Each project has its own `pyproject.toml`, `uv.lock`, `.env.example`, and README. This keeps dependencies and API settings separate for each project.

## Requirements

- Python 3.11 or newer
- [uv](https://docs.astral.sh/uv/) for Python environments and dependencies
- A Groq API key for projects that call an LLM

Check that `uv` is installed:

```powershell
uv --version
```

## Setup

1. Open a project folder in the terminal.
2. Copy `.env.example` to `.env`.
3. Add your Groq API key to `.env`.
4. Install the locked dependencies:

```powershell
uv sync
```
 
## How to run

Run commands from the relevant project folder after completing its setup.

| Project | Command |
|---|---|
| Calling an LLM API | `uv run python main.py` |
| Website Scraper and Summarizer | `uv run python src/app.py` |
| LLM Arena Battle | `uv run python src/app.py` |
| Website Summarizer with LangChain | `uv run python src/summarizer_langchain.py` |
| Chatbot with Memory — Demo | `uv run python src/_1_memory_demo.py` |
| Chatbot with Memory — Chat | `uv run python src/_2_memory_chat.py` |
| Tool-Using Shop Assistant | `uv run python src/app.py` |

See the README inside each project for its objective, API variables, and examples.
