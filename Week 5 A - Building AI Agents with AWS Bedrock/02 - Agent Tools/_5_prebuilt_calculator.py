# What this file does: gives an agent a calculator tool that comes with Strands.

import os

from dotenv import load_dotenv
from strands import Agent
from strands.models.bedrock import BedrockModel
from strands_tools import calculator


load_dotenv()
MODEL_ID = os.getenv("MODEL_ID", "us.amazon.nova-lite-v1:0")


def main() -> None:
    agent = Agent(
        model=BedrockModel(model_id=MODEL_ID),
        tools=[calculator],
        system_prompt="You are a helpful maths assistant.",
    )
    print(agent("What is 42 raised to the power of 9?"))


if __name__ == "__main__":
    main()
