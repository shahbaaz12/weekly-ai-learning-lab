# What this file does: conversational RAG written by hand, so every step is visible.
"""Version 1 of 3. Plain strings, a plain list, and every step called by name."""

import os
import sys

from dotenv import load_dotenv
from langchain_groq import ChatGroq

from _1_vector_store import open_database


load_dotenv()
model = ChatGroq(model=os.getenv("GROQ_MODEL", "openai/gpt-oss-120b"), temperature=0)

# The same follow-up conversation runs in all three chat scripts, so their
# outputs can be compared. Only the first question stands on its own.
CONVERSATION = [
    "What happens in the story about the grasshopper?",
    "Is he lazy at the start?",
    "Who shows him the value of hard work?",
]

# Memory is a list of plain dicts. It exists only while this script runs.
chat_history = []


def history_text() -> str:
    """Flatten the history into lines the prompt can include."""
    return "\n".join(f"{turn['role']}: {turn['content']}" for turn in chat_history)


def contextualize_question(question: str) -> str:
    """Rewrite a follow-up like 'Is he lazy?' into a question the retriever can search."""
    prompt = f"""
Given the conversation history below, rewrite the user's latest question
as a standalone question that can be understood without the history.

Do not answer the question. Only return the rewritten question.

Conversation history:
{history_text()}

Latest question:
{question}

Standalone question:
"""
    return model.invoke(prompt).content.strip()


def generate_answer(question: str, context: str) -> str:
    """Answer from the retrieved context, with the history for tone and continuity."""
    prompt = f"""
You are a helpful assistant.
Answer the user's question using only the provided context.

Conversation history:
{history_text()}

Context:
{context}

Question:
{question}

Answer:
"""
    return model.invoke(prompt).content


def ask(retriever, question: str) -> str:
    """One conversational turn: rewrite, retrieve, answer, remember."""
    standalone_question = contextualize_question(question)
    retrieved = retriever.invoke(standalone_question)
    context = "\n\n".join(doc.page_content for doc in retrieved)
    answer = generate_answer(question, context)

    chat_history.append({"role": "user", "content": question})
    chat_history.append({"role": "assistant", "content": answer})

    print(f"  (searched for: {standalone_question})")
    return answer


def main() -> None:
    # LLM responses can contain Unicode characters, so print them as UTF-8 on Windows.
    sys.stdout.reconfigure(encoding="utf-8")

    retriever = open_database().as_retriever(
        search_type="similarity", search_kwargs={"k": 3}
    )

    for question in CONVERSATION:
        print(f"\nYou: {question}")
        print(f"Bot: {ask(retriever, question)}")

    print(f"\n(History: {len(chat_history)} messages)")


if __name__ == "__main__":
    main()
