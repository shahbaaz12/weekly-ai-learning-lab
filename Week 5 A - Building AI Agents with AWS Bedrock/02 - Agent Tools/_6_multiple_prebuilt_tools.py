# What this file does: combines a web-request tool with a calculator tool.

import os

from dotenv import load_dotenv
from strands import Agent
from strands.models.bedrock import BedrockModel
from strands_tools import calculator, http_request


load_dotenv()
MODEL_ID = os.getenv("MODEL_ID", "us.amazon.nova-lite-v1:0")


def main() -> None:
    agent = Agent(
        model=BedrockModel(model_id=MODEL_ID),
        tools=[http_request, calculator],
        system_prompt="You help with simple data-analysis tasks.",
    )
    print(
        agent(
            "Get the current BTC price from https://api.coinbase.com/v2/prices/BTC-USD/spot "
            "and calculate 10% of that price."
        )
    )


if __name__ == "__main__":
    main()
