# What this file does: merges vector and keyword results with rank fusion, then answers from the merged set.
"""Online RAG stage: two searches, one fused ranking, one grounded answer with sources."""

import os
import sys

from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_groq import ChatGroq

from _1_stores import build_keyword_index, keyword_search, load_chunks, open_database


DEFAULT_QUESTION = "What does error E922 mean and how do I fix it?"

# Each search returns this many candidates before fusion picks the final few.
SEARCH_K = 5
FINAL_K = 3

PROMPT = """
You are a helpful product support assistant.
Answer the question using only the provided context.
If the answer is not present in the context, say that you do not know.

Context:
{context}

Question:
{question}
""".strip()


def reciprocal_rank_fusion(
    result_lists: list[list[Document]], rrf_k: int = 60
) -> list[Document]:
    """Merge ranked lists by rank position, so different score scales do not matter."""
    fused = {}

    for results in result_lists:
        for rank, chunk in enumerate(results, start=1):
            # The same chunk can appear in both lists, so identify it by content.
            key = (chunk.metadata["source"], chunk.metadata["page"], chunk.page_content)
            fused.setdefault(key, {"chunk": chunk, "score": 0.0})
            # A high rank in either list adds more. rrf_k keeps the scores gentle.
            fused[key]["score"] += 1 / (rrf_k + rank)

    ranked = sorted(fused.values(), key=lambda item: item["score"], reverse=True)
    return [item["chunk"] for item in ranked]


def hybrid_search(database, keyword_index, chunks, question: str) -> list[Document]:
    """Run both searches and return the fused top results."""
    vector_results = database.similarity_search(question, k=SEARCH_K)
    keyword_results = keyword_search(keyword_index, chunks, question, k=SEARCH_K)
    return reciprocal_rank_fusion([vector_results, keyword_results])[:FINAL_K]


def main() -> None:
    # LLM responses can contain Unicode characters, so print them as UTF-8 on Windows.
    sys.stdout.reconfigure(encoding="utf-8")
    load_dotenv()

    question = " ".join(sys.argv[1:]) or DEFAULT_QUESTION

    database = open_database()
    chunks = load_chunks(database)
    keyword_index = build_keyword_index(chunks)
    retrieved = hybrid_search(database, keyword_index, chunks, question)

    model = ChatGroq(model=os.getenv("GROQ_MODEL", "openai/gpt-oss-120b"), temperature=0)
    context = "\n\n".join(chunk.page_content for chunk in retrieved)
    answer = model.invoke(PROMPT.format(context=context, question=question)).content

    print(f"Question: {question}\n")
    print(f"Answer: {answer}")

    # Sources make the answer easy to check against the guides.
    print("\nSources:")
    for chunk in retrieved:
        print(f"- {chunk.metadata['source']} (page {chunk.metadata['page']})")


if __name__ == "__main__":
    main()
