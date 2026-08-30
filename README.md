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
├── Week 1 B - Exploring LangChain and Memory/
│   ├── 01 - Website Summarizer with LangChain/
│   ├── 02 - Chatbot with Memory/
│   └── 03 - Tool-Using Shop Assistant/
├── Week 2 A - LangChain Models, Structured Output, and Agents/
│   ├── 01 - Calling Models with LangChain/
│   ├── 02 - Structured Outputs/
│   └── 03 - Working with Agents/
├── Week 2 B - Getting Started with RAG Concepts/
│   ├── 01 - Embeddings and Chunking/
│   └── 02 - Basic RAG with Chroma/
├── Week 3 A - Dockerizing AI Projects/
│   ├── 01 - Dockerize an ML Project/
│   ├── 02 - Dockerize an LLM Project/
│   └── 03 - Dockerize an Agentic Project/
├── Week 4 A - Getting Started with LangGraph/
│   ├── 01 - Basic Graph/
│   ├── 02 - Basic Chatbot/
│   └── 03 - Chatbot with Tools/
├── Week 4 B - Advanced LangGraph Concepts/
│   ├── 01 - ReAct Agent/
│   ├── 02 - Chatbot with Memory/
│   ├── 03 - Streaming Chatbot/
│   └── 04 - Human in the Loop/
├── Week 5 A - Building AI Agents with AWS Bedrock/
│   ├── 01 - First AI Agents/
│   ├── 02 - Agent Tools/
│   └── 03 - Travel Assistant Agent/
├── Week 6 - System Design and Scaling/
├── Week 7 - Scaling Databases/
└── Week 8 - Building an AI Interview Coach/
    └── 01 - InterviewIQ Coach Agent/
```

Each project has its own `pyproject.toml` and `uv.lock`, so dependencies stay
separate. Week 3 uses `requirements.txt` instead, because those projects install
their packages inside Docker images.

## Weeks

| Week | What it covers | Main tools |
|---|---|---|
| 1 A | Send a prompt to an LLM, summarize a webpage, compare two models | OpenAI SDK, Groq, Gradio |
| 1 B | LangChain pipelines, chat memory, a model calling a local tool | LangChain, Groq, Gradio |
| 2 A | One interface for many providers, Pydantic outputs, agents | LangChain, Gemini, Groq |
| 2 B | Embeddings, chunking, a vector database, grounded answers, reranking | Chroma, sentence-transformers, Groq |
| 3 A | Package an ML API, a RAG app, and an agent stack into containers | Docker, Docker Compose, FastAPI |
| 4 A | Graph state, a chatbot node, a chatbot that uses tools | LangGraph, Groq |
| 4 B | ReAct, saved memory, streaming updates, pausing for a human | LangGraph, Groq |
| 5 A | Agents that call tools, class-based tools, async tools, a travel agent | Strands, Amazon Bedrock |
| 6 | Reverse proxies, load balancing, API gateways, CDN, failover | Docker, hosted lessons |
| 7 | Database internals, indexing, replication, partitioning, sharding | Hosted lessons |
| 8 | A mock-interview coach: tool calling, session memory, aggregation, a UI | OpenAI SDK, Groq, Gradio |

## Requirements

- Python 3.11 or newer
- [uv](https://docs.astral.sh/uv/) for Python environments and dependencies
- Docker Desktop, for Week 3 only

API keys, by week:

| Key | Needed for |
|---|---|
| **[Groq API key](https://console.groq.com/keys)** *(free to create)* | Weeks 1 A, 1 B, 2 A, 2 B, 4 A, 4 B, 8 |
| **[Google AI Studio API key](https://aistudio.google.com/app/apikey)** | Week 2 A |
| **OpenAI API key** | Week 3, projects 2 and 3 |
| **AWS credentials with Amazon Nova Lite access in Bedrock** | Week 5 A |

Check that `uv` is installed:

```powershell
uv --version
```

## Setup

Copy `.env.example` to `.env` and add the keys that week needs. The `.env` file
lives in a different place depending on the week:

| Week | Where `.env` goes |
|---|---|
| 1 A, 1 B | Inside each project folder |
| 2 A | Repository root |
| 2 B | Repository root, plus `02 - Basic RAG with Chroma` |
| 3 A | Inside `02 - Dockerize an LLM Project` and `03 - Dockerize an Agentic Project` |
| 4 A, 4 B, 5 A, 8 | In the week folder |

Every `.env` file is ignored by Git. Commit `.env.example`, never the real key.

## How to run

Open a week folder and follow its README. Each one lists the exact command for
every project in that week.

For `uv` projects, the pattern is always the same:

```powershell
uv sync
uv run python <script name>
```

For Week 3, the pattern is:

```powershell
docker compose up -d --build
```

| Week | Start here |
|---|---|
| 1 A | `Week 1 A - Connecting to an LLM/README.md` |
| 1 B | `Week 1 B - Exploring LangChain and Memory/README.md` |
| 2 A | `Week 2 A - LangChain Models, Structured Output, and Agents/README.md` |
| 2 B | `Week 2 B - Getting Started with RAG Concepts/README.md` |
| 3 A | `Week 3 A - Dockerizing AI Projects/README.md` |
| 4 A | `Week 4 A - Getting Started with LangGraph/README.md` |
| 4 B | `Week 4 B - Advanced LangGraph Concepts/README.md` |
| 5 A | `Week 5 A - Building AI Agents with AWS Bedrock/README.md` |
| 6 | `Week 6 - System Design and Scaling/README.md` |
| 7 | `Week 7 - Scaling Databases/README.md` |
| 8 | `Week 8 - Building an AI Interview Coach/README.md` |

See the README inside each project for its objective, API variables, and examples.
