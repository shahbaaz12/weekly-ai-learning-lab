# What this file does: creates the smallest possible AI agent with AWS Bedrock.

import os

from dotenv import load_dotenv
from strands import Agent
from strands.models.bedrock import BedrockModel


load_dotenv()
MODEL_ID = os.getenv("MODEL_ID", "us.amazon.nova-lite-v1:0")


def main() -> None:
    agent = Agent(model=BedrockModel(model_id=MODEL_ID))
    response = agent("Tell me one fun fact about AI agents.")
    print(response)


if __name__ == "__main__":
    main()
