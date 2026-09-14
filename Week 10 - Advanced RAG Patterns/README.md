# Week 10 - Advanced RAG Patterns

## Objective

Go past the basic RAG pipeline from Week 2 B. Each project fixes one thing a
single flat vector search gets wrong: follow-up questions, exact tokens, and
questions that need a different level of detail.

## What I built

1. **Conversational RAG** - Rewrite a follow-up question using the chat history
   before retrieving, built three ways from by-hand to LangChain's chains.
2. **Hybrid RAG** - Combine vector search with a BM25 keyword index using
   reciprocal rank fusion, so error codes and IDs stop getting missed.
3. **Hierarchical RAG** - Store a product catalog at two levels and route each
   question to the right one before searching.

Complete the projects in order. Each one reuses the index-then-query shape from
Week 2 B, so the new idea in each is easy to find.

## Documents

All three projects read from the shared `docs/` folder in this week: ten fables,
ten product guides, and a product catalog with a hierarchy of categories,
products, and variants. `docs/README.md` describes every file and which project
uses it, and explains the 78-question validation set that ships with the
catalog.

## Before running

Create `.env` in this Week 10 folder from `.env.example` and add your Groq key.
It is the same `GROQ_API_KEY` used in the earlier Groq weeks. Embeddings run
locally with a free model, so no other key is needed.

Each project saves its Chroma database in a local `chroma_db` folder that Git
ignores. Run the project's index script once to create it.

## Run a project

Open this Week 10 folder in PowerShell. Run one complete block at a time;
`Push-Location` enters that project and `Pop-Location` returns here afterward.

### 1. Conversational RAG

```powershell
Push-Location "01 - Conversational RAG"
uv sync

uv run python _2_index.py
uv run python _3_manual_chat.py
uv run python _4_template_chat.py
uv run python _5_chain_chat.py
Pop-Location
```

### 2. Hybrid RAG

```powershell
Push-Location "02 - Hybrid RAG"
uv sync

uv run python _2_index.py
uv run python _3_compare_search.py
uv run python _4_hybrid_rag.py
Pop-Location
```

### 3. Hierarchical RAG

```powershell
Push-Location "03 - Hierarchical RAG"
uv sync

uv run python _3_index.py
uv run python _4_inspect_retrieval.py
uv run python _5_hierarchical_rag.py
Pop-Location
```

The `_1_` files, and `_2_vector_store.py` in the third project, are helpers the
other scripts import. You do not run them directly.
