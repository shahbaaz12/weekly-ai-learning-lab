# What this file does: shows a LangGraph agent choosing to call a greeting tool.

import os

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent


load_dotenv()
MODEL_ID = os.getenv("MODEL_ID", "us.amazon.nova-lite-v1:0")


@tool
def greet(name: str) -> str:
    """Greet a person by name."""
    return f"Hello, {name}! Welcome to the world of AI agents."


def main() -> None:
    model = init_chat_model(MODEL_ID, model_provider="bedrock_converse")
    agent = create_react_agent(model=model, tools=[greet])

    response = agent.invoke(
        {"messages": [{"role": "user", "content": "Please greet Alice and Bob."}]}
    )

    # Print each message so the tool-call loop is easy to see.
    for message in response["messages"]:
        print(f"{message.type}: {message.content}")


if __name__ == "__main__":
    main()
