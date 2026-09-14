# What this file does: sends one question to both collections, to show they answer at different levels.

import sys

from _2_vector_store import DETAIL_COLLECTION, SUMMARY_COLLECTION, open_collection


# A broad question. The detail store returns products; the summary store
# returns the one document that already lists them all.
DEFAULT_QUESTION = "Tell me about Climate Control."


def show(title: str, documents) -> None:
    """Print each result's level and the start of its text."""
    print(f"\n=== {title} ===")

    for rank, document in enumerate(documents, start=1):
        meta = document.metadata
        label = meta.get("product_name") or meta.get("variant_name") or meta["subcategory"]
        print(f"\n--- Result {rank} | level: {meta['level']} | {label} ---")
        print(document.page_content[:300])


def main() -> None:
    # Let you test another query without editing the file.
    question = " ".join(sys.argv[1:]) or DEFAULT_QUESTION

    print(f"Question: {question}")

    show("Detail collection", open_collection(DETAIL_COLLECTION).similarity_search(question, k=3))
    show("Summary collection", open_collection(SUMMARY_COLLECTION).similarity_search(question, k=2))


if __name__ == "__main__":
    main()
