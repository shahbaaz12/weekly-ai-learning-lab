# What this file does: runs vector search and keyword search on the same question, side by side.
"""See what each search style finds before combining them."""

import sys

from _1_stores import build_keyword_index, keyword_search, load_chunks, open_database


# An error code is a rare exact token: the case where keyword search shines.
DEFAULT_QUESTION = "E922"


def show(title: str, results) -> None:
    """Print one result list with its sources."""
    print(f"\n=== {title} ===")

    for rank, chunk in enumerate(results, start=1):
        print(f"\n--- Result {rank} | {chunk.metadata['source']} ---")
        print(chunk.page_content)


def main() -> None:
    # Let you test another query without editing the file.
    question = " ".join(sys.argv[1:]) or DEFAULT_QUESTION

    database = open_database()
    chunks = load_chunks(database)
    keyword_index = build_keyword_index(chunks)

    print(f"Question: {question}")

    # Vector search matches meaning, so it can miss an exact code.
    show("Vector search (meaning)", database.similarity_search(question, k=3))

    # Keyword search matches tokens, so it can miss a rephrased question.
    show("Keyword search (exact words)", keyword_search(keyword_index, chunks, question, k=3))


if __name__ == "__main__":
    main()
