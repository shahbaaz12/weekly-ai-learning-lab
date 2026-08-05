# What this file does: builds a chatbot that remembers messages in one thread.

import sys
from typing import Annotated

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict


# Let Windows terminals print all characters returned by the model.
sys.stdout.reconfigure(encoding="utf-8")
load_dotenv()
model = init_chat_model(model="groq:openai/gpt-oss-120b")
memory = MemorySaver()


class ChatState(TypedDict):
    messages: Annotated[list, add_messages]


def chatbot(state: ChatState):
    return {"messages": [model.invoke(state["messages"])]}


def main() -> None:
    builder = StateGraph(ChatState)
    builder.add_node("chatbot", chatbot)
    builder.add_edge(START, "chatbot")
    builder.add_edge("chatbot", END)

    graph = builder.compile(checkpointer=memory)
    config = {"configurable": {"thread_id": "learning-thread"}}

    # Both questions use the same thread, so the second call sees the first one.
    first_response = graph.invoke(
        {"messages": ["My name is Shubham and I enjoy learning AI."]},
        config=config,
    )
    second_response = graph.invoke(
        {"messages": ["What is my name?"]},
        config=config,
    )

    print("First reply:", first_response["messages"][-1].content)
    print("Memory reply:", second_response["messages"][-1].content)


if __name__ == "__main__":
    main()
