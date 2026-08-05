# What this file does: pauses a graph for a human answer and then resumes it.

from typing import Annotated

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.types import Command, interrupt
from typing_extensions import TypedDict


class ApprovalState(TypedDict):
    messages: Annotated[list, add_messages]


def ask_for_approval(state: ApprovalState):
    # interrupt pauses the graph and waits for the value passed to Command(resume=...).
    human_answer = interrupt({"question": "Should this AI answer be approved?"})
    return {"messages": [f"Human answer: {human_answer}"]}


def main() -> None:
    builder = StateGraph(ApprovalState)
    builder.add_node("ask_for_approval", ask_for_approval)
    builder.add_edge(START, "ask_for_approval")
    builder.add_edge("ask_for_approval", END)

    graph = builder.compile(checkpointer=MemorySaver())
    config = {"configurable": {"thread_id": "approval-thread"}}

    paused_state = graph.invoke(
        {"messages": ["The graph is ready for a human decision."]},
        config=config,
    )
    question = paused_state["__interrupt__"][0].value["question"]
    print(f"Question for the human: {question}")

    # In a real app, this value would come from a person using the interface.
    final_state = graph.invoke(Command(resume="Yes, approved."), config=config)
    print(final_state["messages"][-1].content)


if __name__ == "__main__":
    main()
