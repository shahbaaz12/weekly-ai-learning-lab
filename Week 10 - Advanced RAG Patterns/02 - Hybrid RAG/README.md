# Hybrid RAG

## Objective

Learn why vector search alone misses exact tokens like error codes and product
IDs, and how a keyword index fills that gap.

## What I built

A support assistant over ten smart-home product guides. It searches the same
chunks two ways, merges the two rankings, and answers from the merged set.

## How it works

1. `_2_index.py` chunks the PDFs and saves the embeddings in Chroma, as before.
2. At query time, the chunks are read back out of Chroma to build a BM25 index.
3. Vector search finds chunks with similar *meaning*.
4. BM25 finds chunks containing the same *words*.
5. Reciprocal rank fusion merges the two lists by rank position.
6. The top fused chunks become the context for the answer.

Building BM25 from what Chroma holds means both indexes cover exactly the same
chunks, so a result from either side is always a real stored chunk.

## Why both

| Question | Vector search | Keyword search |
|---|---|---|
| `E922` | Three unrelated products | The right product, twice |
| `vacuum will not move` | The right product, three times | A thermostat first, then the right product |

Run `_3_compare_search.py` with each of those to see it. An error code is a
rare exact token, so only keyword matching catches it. A rephrased complaint
uses common words the wrong guide also contains, so meaning ranks it better.

## Why rank fusion

BM25 scores and cosine distances are on different scales, so adding them is
meaningless. Reciprocal rank fusion ignores the scores and uses each chunk's
*position* in each list: `1 / (60 + rank)`. A chunk near the top of both lists
wins. A chunk in only one list can still make it.

## Setup

`.env` lives in the Week 10 folder and needs `GROQ_API_KEY`. Only `_4_` calls
the model; indexing and both searches run locally.

The product guides are in `../docs/products/`, one PDF per device. See
`../docs/README.md` for the full product line and the error codes.

## Run

```powershell
uv sync

uv run python _2_index.py
uv run python _3_compare_search.py
uv run python _4_hybrid_rag.py
```

Both query scripts accept a question after the filename:

```powershell
uv run python _3_compare_search.py "vacuum will not move"
uv run python _4_hybrid_rag.py "What does E701 mean?"
```

`_1_stores.py` is a helper the other scripts import, so you do not run it
directly.

## Key idea

Vector search and keyword search fail on different questions, so together they
fail on fewer. Hybrid retrieval is the usual first fix when a RAG system keeps
missing the exact IDs, codes, and names that users type.
