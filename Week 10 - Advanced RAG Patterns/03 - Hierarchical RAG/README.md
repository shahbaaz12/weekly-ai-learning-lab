# Hierarchical RAG

## Objective

Learn how to answer both a detailed question and a broad question over the
same data, by storing it at more than one level and choosing the level first.

## What I built

A catalog assistant over a structured product catalog. A router picks the
level, one retriever searches it, and the answer names its sources.

```text
Category -> Subcategory -> Product -> Variant
```

## How it works

1. `_1_documents.py` turns the catalog JSON into documents at three levels.
2. Products and variants go into the **detail** collection.
3. One summary per subcategory goes into the **summary** collection.
4. A router asks the model one thing: does this question need DETAIL or SUMMARY?
5. Only the matching collection is searched.
6. The answer is written from that context, with the retrieved sources listed.

The router never answers the question. It only chooses where to look.

## Why two levels

| Question | Route | What comes back |
|---|---|---|
| Which AeroTherm variant adds humidity control? | DETAIL | The `HCL-101-P` variant document |
| Compare all Climate Control products. | SUMMARY | One document that already lists both products |

Run `_4_inspect_retrieval.py` to send a broad question to *both* collections
and see the difference. The detail store returns two products and a stray
variant. The summary store returns the one document written for that question.

## Why the documents are flattened

The JSON holds dicts and lists. `_1_documents.py` writes them out as lines
(`- key: value`) before embedding, so the stored text reads like a spec sheet.
A retrieved document can be printed and understood as-is, and swapping the
embedding model later does not change what was embedded.

Nothing is chunked. Each product, variant, or summary is already one complete
document, so splitting it would only separate facts that belong together.

## Setup

`.env` lives in the Week 10 folder and needs `GROQ_API_KEY`. Only `_5_` calls
the model; indexing and inspection run locally.

The catalog is `../docs/products2/Hierarchical_Product_Catalog.json`. Beside it,
`Hierarchical_RAG_Validation_Questions.json` holds 78 questions with expected
answers and the level each should route to, which is a ready-made way to test
the router. See `../docs/README.md` for the breakdown.

## Run

```powershell
uv sync

uv run python _3_index.py
uv run python _4_inspect_retrieval.py
uv run python _5_hierarchical_rag.py
```

Both query scripts accept a question after the filename:

```powershell
uv run python _5_hierarchical_rag.py "What does CLM-E214 mean?"
uv run python _5_hierarchical_rag.py "Summarise the products under Water Protection."
```

`_1_documents.py` and `_2_vector_store.py` are helpers the other scripts
import, so you do not run them directly.

## Key idea

A flat store answers every question from the same-sized pieces, so it is
either too fine for a comparison or too coarse for a spec. Storing a summary
level alongside the detail level, and routing before retrieving, lets one
system answer both kinds of question well.

## Next

The router only knows DETAIL and SUMMARY. A question like "compare Climate
Control products and say which supports humidity" needs both. A HYBRID route
that searches both collections and merges the results is the natural next step.
