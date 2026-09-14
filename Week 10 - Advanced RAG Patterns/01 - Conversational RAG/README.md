# Conversational RAG

## Objective

Learn how RAG handles a follow-up question like "Is he lazy?", where the
retriever has no idea who "he" is unless the conversation is used first.

## What I built

The same chatbot three times, over ten short fables in PDF form. Each version
does the same four steps. What changes is how much of it LangChain does for you.

## How it works

1. `_2_index.py` reads every PDF page, chunks it, and saves the embeddings in Chroma.
2. A follow-up question is rewritten into a standalone one using the chat history.
3. The standalone question goes to the retriever, not the original one.
4. The model answers from the retrieved chunks, with the history for continuity.
5. Both sides of the turn are added to the history for the next question.

Step 2 is the whole idea. Without it, "Who shows him the value of hard work?"
retrieves nothing useful, because the chunk about the ant never says "him".

## The three versions

| Script | What does the work |
|---|---|
| `_3_manual_chat.py` | Plain f-strings and a list of dicts. Every step is a function you can read. |
| `_4_template_chat.py` | `ChatPromptTemplate` and `MessagesPlaceholder` build the prompts. History is real message objects. |
| `_5_chain_chat.py` | `create_history_aware_retriever`, `create_stuff_documents_chain`, and `create_retrieval_chain` replace the hand-written steps. |

The algorithm never changes. `_3_` shows it, `_5_` packages it.

| Written by hand in `_3_` | Handled by LangChain in `_5_` |
|---|---|
| `contextualize_question()` then `retriever.invoke()` | `create_history_aware_retriever` |
| `"\n\n".join(doc.page_content ...)` then `generate_answer()` | `create_stuff_documents_chain` |
| the sequence inside `ask()` | `create_retrieval_chain` |

`_3_` and `_4_` print the rewritten question on each turn, so you can see the
history doing its job before the retriever runs.

## Setup

`.env` lives in the Week 10 folder and needs `GROQ_API_KEY`. Embeddings run
locally, so nothing else is required.

The fables are in `../docs/smallStories/`, one PDF each. See `../docs/README.md`
for what else is in that folder.

## Run

```powershell
uv sync

uv run python _2_index.py
uv run python _3_manual_chat.py
uv run python _4_template_chat.py
uv run python _5_chain_chat.py
```

`_1_vector_store.py` is a helper the other scripts import, so you do not run it
directly. Change the questions in `CONVERSATION` to try your own follow-ups.

## Key idea

Memory alone is not enough for RAG. The history has to be used *before*
retrieval, to turn the follow-up into something the vector store can actually
search for. The three scripts are the same pipeline at three levels of
abstraction, so you can pick the level you want to work at.
