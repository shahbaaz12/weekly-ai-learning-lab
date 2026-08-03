# What this file does: builds a two-step LangGraph and passes shared state through it.

from typing import Annotated

from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict


class GraphState(TypedDict):
    # id increases at each node, while messages are appended to the state.
    id: int
    messages: Annotated[list, add_messages]


def step_one(state: GraphState):
    return {"id": state["id"] + 1, "messages": ["Step 1 completed"]}


def step_two(state: GraphState):
    return {"id": state["id"] + 1, "messages": ["Step 2 completed"]}


def main() -> None:
    # Build the path: START -> step_one -> step_two -> END.
    builder = StateGraph(GraphState)
    builder.add_node("step_one", step_one)
    builder.add_node("step_two", step_two)
    builder.add_edge(START, "step_one")
    builder.add_edge("step_one", "step_two")
    builder.add_edge("step_two", END)

    graph = builder.compile()
    response = graph.invoke({"id": 0, "messages": ["Begin"]})

    print(f"Final id: {response['id']}")
    print("Messages:")
    for message in response["messages"]:
        print(f"- {message.content}")


if __name__ == "__main__":
    main()
