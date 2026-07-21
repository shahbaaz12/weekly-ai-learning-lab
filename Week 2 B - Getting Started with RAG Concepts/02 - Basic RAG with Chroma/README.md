# Basic RAG with Chroma

## Objective

Build a small Retrieval-Augmented Generation (RAG) pipeline in clear stages:

1. Split source documents into chunks.
2. Turn the chunks into local embeddings.
3. Store the chunks and embeddings in a persistent Chroma database.
4. Inspect what retrieval found before involving an LLM.
5. Ask a Groq model to answer from retrieved context only.
6. Compare normal vector retrieval with optional cross-encoder reranking.

## Setup

Install dependencies after opening this folder:

```powershell
uv sync
```

Copy `.env.example` to `.env`, then add your Groq key. The first three scripts do
not require the key; only `_5_rag.py` does.

```powershell
Copy-Item .env.example .env
```

## Run order

```powershell
uv run python _3_index.py
uv run python _4_inspect_retrieval.py
uv run python _5_rag.py
uv run python _6_rerank.py
```

## Ask your own question

Each query script accepts a question after the filename. If you do not provide
one, the script uses its built-in default question.

```powershell
# Inspect the chunks Chroma finds before calling an LLM.
uv run python _4_inspect_retrieval.py "Do you offer free delivery?"

# Ask the grounded RAG answerer about the stored company-policy data.
uv run python _5_rag.py "What time does the Bangalore office open?"

# Compare the reranker's best results for a return-policy question.
uv run python _6_rerank.py "What is needed to return an item?"
```

The question is read from the command line with `sys.argv[1:]`, so every word
after the script name becomes part of the question.

## Key idea

`_3_index.py` is the offline stage: run it when the documents change. The other
scripts are the online stage: each question retrieves from the saved `chroma_db`
folder in milliseconds.
