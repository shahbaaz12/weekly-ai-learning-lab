# Week 2 B - Getting Started with RAG Concepts

## Objective

Learn how Retrieval-Augmented Generation (RAG) gives an LLM access to your own
documents instead of making it guess. This week focuses on the foundations:
embeddings, chunking, vector databases, retrieval, grounded answers, and
reranking.

## Projects

1. **Embeddings and Chunking** — Turn text into vectors, compare meaning with cosine similarity, and split documents into useful overlapping chunks.
2. **Basic RAG with Chroma** — Store chunks in a local vector database, inspect retrieval results, create grounded answers, and try reranking.

Complete the projects in order. The second project deliberately uses a tiny local
dataset so you can see every RAG stage before moving on to PDFs or a user
interface.

## Setup

The first project runs completely locally and does not need an API key. In the
second project, indexing and retrieval also run locally; only the grounded-answer
script needs a Groq API key.

Copy the repository-root `.env.example` file to `.env`, then add your Groq key:

```env
GROQ_API_KEY=your_groq_api_key_here
```

The `.env` file is ignored by Git. Commit `.env.example`, never the real key.

## Run a project

Open this Week 2 B folder in PowerShell. Run one complete block at a time;
`Push-Location` enters that project and `Pop-Location` returns here afterward.

### 1. Embeddings and Chunking

```powershell
Push-Location "01 - Embeddings and Chunking"
uv sync

uv run python _1_embeddings.py
uv run python _2_chunking.py
Pop-Location
```

### 2. Basic RAG with Chroma

```powershell
Push-Location "02 - Basic RAG with Chroma"
uv sync

# Offline stage: create the local Chroma database.
uv run python _3_index.py

# Online stage: see which chunks are retrieved for a question.
uv run python _4_inspect_retrieval.py

# Requires GROQ_API_KEY in the repository-root .env file.
uv run python _5_rag.py

# Optional improvement: rerank the vector-search candidates.
uv run python _6_rerank.py
Pop-Location
```

`_1_documents.py` stores the sample company-policy data, and
`_2_vector_store.py` holds the shared embedding-model and Chroma configuration.
They are helper files, so you do not run them directly.
