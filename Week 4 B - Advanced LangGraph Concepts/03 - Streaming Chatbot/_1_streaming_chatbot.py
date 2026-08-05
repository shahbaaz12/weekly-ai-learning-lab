# What this file does: streams each chatbot update from a LangGraph conversation.

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


def stream_reply(graph, message: str, config: dict) -> None:
    print(f"Question: {message}")
    # Stream the update created by the chatbot node.
    for chunk in graph.stream(
        {"messages": [message]},
        config=config,
        stream_mode="updates",
    ):
        answer = chunk["chatbot"]["messages"][-1].content
        print(f"Answer: {answer}")


def main() -> None:
    builder = StateGraph(ChatState)
    builder.add_node("chatbot", chatbot)
    builder.add_edge(START, "chatbot")
    builder.add_edge("chatbot", END)

    graph = builder.compile(checkpointer=memory)
    config = {"configurable": {"thread_id": "streaming-thread"}}

    stream_reply(graph, "My name is Shubham and I enjoy games.", config)
    stream_reply(graph, "What do I enjoy?", config)


if __name__ == "__main__":
    main()
