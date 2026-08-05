# What this file does: builds a ReAct-style graph that can use a multiply tool.

import sys
from typing import Annotated

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


class AgentState(TypedDict):
    messages: Annotated[list, add_messages]


def call_model(state: AgentState):
    # The model can answer directly or ask the graph to run a tool.
    return {"messages": [model_with_tools.invoke(state["messages"])]}


def main() -> None:
    builder = StateGraph(AgentState)
    builder.add_node("model", call_model)
    builder.add_node("tools", ToolNode(tools))
    builder.add_edge(START, "model")
    builder.add_conditional_edges("model", tools_condition)
    builder.add_edge("tools", "model")

    graph = builder.compile()
    response = graph.invoke(
        {"messages": ["Use the multiply tool to calculate 7 multiplied by 8."]}
    )

    print("Messages created by the graph:")
    for message in response["messages"]:
        print(f"- {message.type}: {message.content}")


if __name__ == "__main__":
    main()
