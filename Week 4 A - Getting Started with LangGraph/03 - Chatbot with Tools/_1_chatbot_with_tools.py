# What this file does: lets a LangGraph chatbot call a local multiply tool.

from typing import Annotated
import sys

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain.tools import tool
from langgraph.graph import START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from typing_extensions import TypedDict


# Let Windows terminals print all characters returned by the model.
sys.stdout.reconfigure(encoding="utf-8")
load_dotenv()


@tool
def multiply(a: int, b: int) -> int:
    """Multiply two integers."""
    return a * b


tools = [multiply]
model = init_chat_model(model="groq:openai/gpt-oss-120b")
model_with_tools = model.bind_tools(tools)


class ToolChatState(TypedDict):
    messages: Annotated[list, add_messages]


def call_model(state: ToolChatState):
    # The model either answers directly or asks LangGraph to run a tool.
    return {"messages": [model_with_tools.invoke(state["messages"])]}


def main() -> None:
    builder = StateGraph(ToolChatState)
    builder.add_node("model", call_model)
    builder.add_node("tools", ToolNode(tools))
    builder.add_edge(START, "model")
    builder.add_conditional_edges("model", tools_condition)
    builder.add_edge("tools", "model")

    graph = builder.compile()
    response = graph.invoke({"messages": ["What is 2 multiplied by 6?"]})

    print(response["messages"][-1].content)


if __name__ == "__main__":
    main()
