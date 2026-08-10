# What this file does: lets an agent use a tip-calculator tool.

import os

from dotenv import load_dotenv
from strands import Agent, tool
from strands.models.bedrock import BedrockModel


load_dotenv()
MODEL_ID = os.getenv("MODEL_ID", "us.amazon.nova-lite-v1:0")


@tool
def calculate_tip(bill_amount: float, tip_percentage: float, num_people: int = 1) -> dict:
    """Calculate a tip and split the total bill between people."""
    tip = bill_amount * tip_percentage / 100
    total = bill_amount + tip

    return {
        "bill": bill_amount,
        "tip": round(tip, 2),
        "total": round(total, 2),
        "per_person": round(total / num_people, 2),
    }


def main() -> None:
    agent = Agent(
        model=BedrockModel(model_id=MODEL_ID),
        tools=[calculate_tip],
    )
    print(agent("The bill is $85. Add a 20% tip and split it between 4 people."))


if __name__ == "__main__":
    main()
