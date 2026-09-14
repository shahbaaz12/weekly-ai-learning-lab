# What this file does: the same conversational RAG, using LangChain's ready-made retrieval chains.
"""Version 3 of 3. The rewrite, retrieve, and answer steps become three LangChain components."""

import os
import sys

from dotenv import load_dotenv
from langchain_classic.chains import create_history_aware_retriever, create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
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

chat_history = []

# These chains expect the user's question under the key "input".
contextualize_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Given the chat history and the latest user question, rewrite the "
            "question as a standalone question that can be understood without "
            "the history. Do not answer it. Only rewrite it if necessary.",
        ),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)

qa_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant. Answer the user's question using only "
            "the retrieved context. If the answer is not in the context, say you "
            "do not know.\n\nContext:\n{context}",
        ),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)


def build_chain(retriever):
    """Assemble the three components into one conversational RAG chain."""
    # 1. Rewrites the question with the history, then retrieves. Replaces
    #    contextualize_question() and retriever.invoke() from _3_ and _4_.
    history_aware_retriever = create_history_aware_retriever(
        model, retriever, contextualize_prompt
    )

    # 2. Joins the retrieved documents into {context} and asks the model.
    #    Replaces the "\n\n".join(...) and generate_answer() steps.
    question_answer_chain = create_stuff_documents_chain(model, qa_prompt)

    # 3. Connects retrieval to answering.
    return create_retrieval_chain(history_aware_retriever, question_answer_chain)


def ask(rag_chain, question: str) -> str:
    """One conversational turn. The chain does the rewrite, retrieve, and answer."""
    response = rag_chain.invoke({"input": question, "chat_history": chat_history})
    answer = response["answer"]

    chat_history.append(HumanMessage(content=question))
    chat_history.append(AIMessage(content=answer))

    return answer


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")

    retriever = open_database().as_retriever(
        search_type="similarity", search_kwargs={"k": 3}
    )
    rag_chain = build_chain(retriever)

    for question in CONVERSATION:
        print(f"\nYou: {question}")
        print(f"Bot: {ask(rag_chain, question)}")

    print(f"\n(History: {len(chat_history)} messages)")


if __name__ == "__main__":
    main()
