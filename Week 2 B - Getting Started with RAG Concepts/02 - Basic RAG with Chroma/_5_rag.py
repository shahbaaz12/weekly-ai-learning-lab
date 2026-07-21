# What this file does: retrieves relevant chunks and asks Groq to answer using only that context.
"""Online RAG stage: retrieve saved chunks, then answer from them only."""

import os
import sys

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

from _2_vector_store import open_database


DEFAULT_QUESTION = "How long do I have to return an item?"

PROMPT = ChatPromptTemplate.from_template(
    """
Answer the question using only the context below.
If the answer is not in the context, say: "I don't know based on the stored documents."
Be concise and do not invent policy details.

Context:
{context}

Question: {question}
""".strip()
)


def answer_question(question: str) -> str:
    """Retrieve three chunks, then ask the LLM to answer from those chunks."""
    database = open_database()
    chunks = database.similarity_search(question, k=3)
    # This is the only document text the LLM receives as evidence for its answer.
    context = "\n\n".join(chunk.page_content for chunk in chunks)

    model = ChatGroq(
        model=os.getenv("GROQ_MODEL", "openai/gpt-oss-120b"),
        temperature=0,  # Prefer consistent, factual phrasing for this demo.
    )

    # The prompt formats the context and question before passing them to Groq.
    chain = PROMPT | model
    response = chain.invoke({"context": context, "question": question})
    return response.content


def main() -> None:
    # LLM responses can contain Unicode characters, so print them as UTF-8 on Windows.
    sys.stdout.reconfigure(encoding="utf-8")
    load_dotenv()

    question = " ".join(sys.argv[1:]) or DEFAULT_QUESTION
    print(f"Question: {question}\n")
    print(f"Answer: {answer_question(question)}")


if __name__ == "__main__":
    main()
