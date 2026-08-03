# What this file does: runs a Groq chat model inside one LangGraph chatbot node.

from operator import add
import sys
from typing import Annotated

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict


# Let Windows terminals print all characters returned by the model.
sys.stdout.reconfigure(encoding="utf-8")
load_dotenv()
model = init_chat_model(model="groq:openai/gpt-oss-120b")


class ChatState(TypedDict):
    log: Annotated[list[str], add]
    messages: Annotated[list, add_messages]


def chatbot(state: ChatState):
    # The model reads the current messages and adds one AI response.
    response = model.invoke(state["messages"])
    return {"messages": [response], "log": ["chatbot node executed"]}


def main() -> None:
    builder = StateGraph(ChatState)
    builder.add_node("chatbot", chatbot)
    builder.add_edge(START, "chatbot")
    builder.add_edge("chatbot", END)

    graph = builder.compile()
    response = graph.invoke({"log": ["Begin"], "messages": ["Hi, LangGraph!"]})

    print(response["messages"][-1].content)
    print(response["log"][-1])


if __name__ == "__main__":
    main()
