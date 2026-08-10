# What this file does: gives an agent a custom tool to check product inventory.

import os

from dotenv import load_dotenv
from strands import Agent, tool
from strands.models.bedrock import BedrockModel


load_dotenv()
MODEL_ID = os.getenv("MODEL_ID", "us.amazon.nova-lite-v1:0")


@tool
def check_inventory(product_id: str) -> str:
    """Check the stock available for a product ID."""
    inventory = {
        "PROD-123": 15,
        "PROD-456": 0,
        "PROD-789": 8,
    }
    quantity = inventory.get(product_id, 0)

    if quantity > 0:
        return f"{product_id} is in stock with {quantity} units."
    return f"{product_id} is out of stock."


def main() -> None:
    agent = Agent(
        model=BedrockModel(model_id=MODEL_ID),
        tools=[check_inventory],
    )
    print(agent("Can I order PROD-123 right now?"))


if __name__ == "__main__":
    main()
