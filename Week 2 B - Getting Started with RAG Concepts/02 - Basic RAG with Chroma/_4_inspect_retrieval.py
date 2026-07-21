# What this file does: shows the chunks Chroma retrieves before an LLM is asked to answer.
"""See which chunks vector search retrieves before asking an LLM to answer."""

import sys

from _2_vector_store import open_database


DEFAULT_QUESTION = "How long do I have to return an item?"


def main() -> None:
    # Let you test another query without editing the file.
    question = " ".join(sys.argv[1:]) or DEFAULT_QUESTION
    database = open_database()

    # Chroma embeds the question, then returns nearby chunk embeddings.
    # Its raw distance is lower when the chunk is a closer semantic match.
    results = database.similarity_search_with_score(question, k=3)

    print(f"Question: {question}")
    print("\nRetrieved chunks (lower distance is better):")

    # Inspecting these chunks is the fastest way to diagnose a weak RAG answer.
    for rank, (chunk, distance) in enumerate(results, start=1):
        print(f"\n--- Result {rank} | distance: {distance:.3f} ---")
        print(chunk.page_content)


if __name__ == "__main__":
    main()
