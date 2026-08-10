# What this file does: lets an agent check three warehouses with an async tool.

import asyncio
import os
import time

from dotenv import load_dotenv
from strands import Agent, tool
from strands.models.bedrock import BedrockModel


load_dotenv()
MODEL_ID = os.getenv("MODEL_ID", "us.amazon.nova-lite-v1:0")


@tool
async def check_warehouse_inventory(product_id: str, warehouse: str) -> dict:
    """Check one product's inventory in one warehouse."""
    await asyncio.sleep(2)

    inventory = {
        "east": {"PROD-123": 45},
        "west": {"PROD-123": 30},
        "central": {"PROD-123": 60},
    }
    quantity = inventory[warehouse].get(product_id, 0)

    return {"warehouse": warehouse, "product_id": product_id, "quantity": quantity}


async def main() -> None:
    agent = Agent(
        model=BedrockModel(model_id=MODEL_ID),
        tools=[check_warehouse_inventory],
    )

    start_time = time.time()
    response = await agent.invoke_async(
        "Can we ship 100 units of PROD-123? Check east, west, and central warehouses."
    )
    elapsed_time = time.time() - start_time

    print(response)
    print(f"Total time: {elapsed_time:.1f} seconds")


if __name__ == "__main__":
    asyncio.run(main())
