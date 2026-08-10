# What this file does: turns a Python function into a tool an agent can call.

import os

import requests
from dotenv import load_dotenv
from strands import Agent, tool
from strands.models.bedrock import BedrockModel


load_dotenv()
MODEL_ID = os.getenv("MODEL_ID", "us.amazon.nova-lite-v1:0")


@tool
def check_server_status(server_url: str) -> str:
    """Check whether a server responds at the given URL."""
    response = requests.get(server_url, timeout=5)
    return f"Server responded with status code {response.status_code}."


def main() -> None:
    agent = Agent(
        model=BedrockModel(model_id=MODEL_ID),
        tools=[check_server_status],
    )
    print(agent("Check whether https://httpbin.org/get is running."))


if __name__ == "__main__":
    main()
