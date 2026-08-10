# What this file does: groups related inventory tools inside one class.

import os

from dotenv import load_dotenv
from strands import Agent, tool
from strands.models.bedrock import BedrockModel


load_dotenv()
MODEL_ID = os.getenv("MODEL_ID", "us.amazon.nova-lite-v1:0")


class InventoryTools:
    def __init__(self):
        # Both tools use this same product data.
        self.products = {
            "PROD-123": {"name": "Wireless Mouse", "quantity": 15, "price": 29.99},
            "PROD-456": {"name": "USB-C Hub", "quantity": 0, "price": 49.99},
        }

    @tool
    def check_stock(self, product_id: str) -> str:
        """Check a product's stock level."""
        product = self.products.get(product_id)
        return f"{product['name']}: {product['quantity']} units at ${product['price']}"

    @tool
    def update_stock(self, product_id: str, quantity: int) -> str:
        """Update a product's stock quantity."""
        self.products[product_id]["quantity"] = quantity
        return f"Updated {product_id} to {quantity} units."


def main() -> None:
    inventory = InventoryTools()
    agent = Agent(
        model=BedrockModel(model_id=MODEL_ID),
        tools=[inventory.check_stock, inventory.update_stock],
    )
    print(agent("Set PROD-456 stock to 25 units, then tell me its new stock level."))


if __name__ == "__main__":
    main()
