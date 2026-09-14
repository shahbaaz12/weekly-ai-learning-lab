# What this file does: routes each question to the right level of the catalog, then answers with sources.
"""Online RAG stage: route -> retrieve from one level -> answer from that context."""

import os
import sys

from dotenv import load_dotenv
from langchain_groq import ChatGroq

from _2_vector_store import DETAIL_COLLECTION, SUMMARY_COLLECTION, open_collection


DEFAULT_QUESTION = "Which AeroTherm variant adds humidity control?"

ROUTER_PROMPT = """
Classify the user question into exactly one category.

DETAIL: the question asks about a specific product, variant, specification,
price, error code, setup step, usage instruction, or troubleshooting detail.

SUMMARY: the question asks to compare, summarise, list, or analyse multiple
products, a category, or a subcategory.

Return only one word: DETAIL or SUMMARY.

Question:
{question}
""".strip()

ANSWER_PROMPT = """
You are a helpful product-catalog assistant.
Answer the question using only the provided context.
If the context does not contain enough information, say:
"I could not find enough information in the catalog."

Retrieval level used: {route}

Context:
{context}

Question:
{question}
""".strip()


def route_question(model, question: str) -> str:
    """Ask the model which level of the catalog the question needs."""
    answer = model.invoke(ROUTER_PROMPT.format(question=question)).content.strip().upper()

    # The router picks the level. It never answers the question itself.
    return "SUMMARY" if "SUMMARY" in answer else "DETAIL"


def retrieve(route: str, question: str) -> list:
    """Search only the collection that matches the route."""
    if route == "SUMMARY":
        return open_collection(SUMMARY_COLLECTION).similarity_search(question, k=2)

    return open_collection(DETAIL_COLLECTION).similarity_search(question, k=3)


def describe_source(document) -> str:
    """One readable line per retrieved document, so an answer can be checked."""
    meta = document.metadata

    if meta["level"] == "product":
        return f"product {meta['product_id']} - {meta['product_name']}"

    if meta["level"] == "variant":
        return (
            f"variant {meta['variant_id']} - {meta['variant_name']} "
            f"(of {meta['parent_product_name']})"
        )

    return f"subcategory summary - {meta['category']} / {meta['subcategory']}"


def main() -> None:
    # LLM responses can contain Unicode characters, so print them as UTF-8 on Windows.
    sys.stdout.reconfigure(encoding="utf-8")
    load_dotenv()

    question = " ".join(sys.argv[1:]) or DEFAULT_QUESTION
    model = ChatGroq(model=os.getenv("GROQ_MODEL", "openai/gpt-oss-120b"), temperature=0)

    route = route_question(model, question)
    retrieved = retrieve(route, question)
    context = "\n\n".join(document.page_content for document in retrieved)

    answer = model.invoke(
        ANSWER_PROMPT.format(route=route, context=context, question=question)
    ).content

    print(f"Question: {question}")
    print(f"Route: {route}\n")
    print(f"Answer: {answer}")

    print("\nSources:")
    for document in retrieved:
        print(f"- {describe_source(document)}")


if __name__ == "__main__":
    main()
