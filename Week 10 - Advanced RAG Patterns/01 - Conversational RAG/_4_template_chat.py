# What this file does: the same conversational RAG, with prompt templates and real message objects.
"""Version 2 of 3. Same steps as _3_, but LangChain owns the prompt formatting."""

import os
import sys

from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_groq import ChatGroq

from _1_vector_store import open_database


load_dotenv()
model = ChatGroq(model=os.getenv("GROQ_MODEL", "openai/gpt-oss-120b"), temperature=0)

CONVERSATION = [
    "What happens in the story about the grasshopper?",
    "Is he lazy at the start?",
    "Who shows him the value of hard work?",
]

# Memory is now a list of HumanMessage and AIMessage objects, which is what
# MessagesPlaceholder expects to insert into the prompt.
chat_history = []

# The placeholder is where the earlier turns are inserted, so the prompt no
# longer needs the history flattened into a string by hand.
contextualize_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Rewrite the user's latest question as a standalone question that "
            "can be understood without the conversation history. "
            "Do not answer it. Only return the rewritten question.",
        ),
        MessagesPlaceholder("chat_history"),
        ("human", "{question}"),
    ]
)

answer_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant. Answer the user's question using only "
            "the provided context.\n\nContext:\n{context}",
        ),
        MessagesPlaceholder("chat_history"),
        ("human", "{question}"),
    ]
)

# LangChain pipeline: prompt -> model, one for each job
contextualize_chain = contextualize_prompt | model
answer_chain = answer_prompt | model


def ask(retriever, question: str) -> str:
    """One conversational turn: rewrite, retrieve, answer, remember."""
    standalone_question = contextualize_chain.invoke(
        {"chat_history": chat_history, "question": question}
    ).content.strip()

    retrieved = retriever.invoke(standalone_question)
    context = "\n\n".join(doc.page_content for doc in retrieved)

    answer = answer_chain.invoke(
        {"chat_history": chat_history, "context": context, "question": question}
    ).content

    chat_history.append(HumanMessage(content=question))
    chat_history.append(AIMessage(content=answer))

    print(f"  (searched for: {standalone_question})")
    return answer


def main() -> None:
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
