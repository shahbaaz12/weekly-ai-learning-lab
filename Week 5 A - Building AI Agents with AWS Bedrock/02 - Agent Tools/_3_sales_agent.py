# What this file does: lets an agent combine small tools to prepare a sales summary.

import os

from dotenv import load_dotenv
from strands import Agent, tool
from strands.models.bedrock import BedrockModel


load_dotenv()
MODEL_ID = os.getenv("MODEL_ID", "us.amazon.nova-lite-v1:0")


@tool
def get_sales_data(quarter: str) -> dict:
    """Get sales data for a quarter."""
    return {"quarter": quarter, "revenue": 1250000, "deals": 47}


@tool
def analyze_sales(revenue: int, deals: int, quarter: str) -> str:
    """Calculate the average deal size from sales data."""
    average_deal = revenue / deals
    return f"Q{quarter}: ${revenue:,} revenue, {deals} deals, ${average_deal:,.0f} average deal."


@tool
def send_email(to: str, subject: str, body: str) -> str:
    """Send a sales-summary email."""
    return f"Email sent to {to} with subject: {subject}"


def main() -> None:
    agent = Agent(
        model=BedrockModel(model_id=MODEL_ID),
        tools=[get_sales_data, analyze_sales, send_email],
    )
    print(agent("Get Q4 sales data, create a summary, and email it to the sales team."))


if __name__ == "__main__":
    main()
