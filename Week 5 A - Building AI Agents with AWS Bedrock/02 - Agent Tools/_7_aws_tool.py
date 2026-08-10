# What this file does: lets an agent use an AWS tool to list S3 buckets.

import os

from dotenv import load_dotenv
from strands import Agent
from strands.models.bedrock import BedrockModel
from strands_tools import use_aws


load_dotenv()
MODEL_ID = os.getenv("MODEL_ID", "us.amazon.nova-lite-v1:0")


def main() -> None:
    agent = Agent(
        model=BedrockModel(model_id=MODEL_ID),
        tools=[use_aws],
        system_prompt="You are an AWS assistant. Only use read-only AWS actions.",
    )
    print(agent("List all S3 buckets in my account."))


if __name__ == "__main__":
    main()
