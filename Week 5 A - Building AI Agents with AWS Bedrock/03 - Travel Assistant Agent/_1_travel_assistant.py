# What this file does: builds a travel agent with weather, packing, and cost tools.

import os
import sys

from dotenv import load_dotenv
from strands import Agent, tool
from strands.models.bedrock import BedrockModel
from strands_tools import calculator


load_dotenv()
MODEL_ID = os.getenv("MODEL_ID", "us.amazon.nova-lite-v1:0")


@tool
def get_weather_forecast(city: str, days: int) -> dict:
    """Get a weather forecast for a city and trip length."""
    forecasts = {
        "goa": {"high_c": 32, "low_c": 26, "conditions": "humid with occasional showers"},
        "bangalore": {"high_c": 27, "low_c": 18, "conditions": "mild with evening rain"},
        "jaipur": {"high_c": 38, "low_c": 25, "conditions": "hot and dry"},
        "manali": {"high_c": 14, "low_c": 3, "conditions": "cold with possible snow"},
    }
    return {"city": city, "days": days, **forecasts.get(city.lower(), forecasts["goa"])}


@tool
def suggest_packing_list(high_c: int, low_c: int, days: int, conditions: str) -> list:
    """Suggest items to pack using temperature, trip length, and weather."""
    items = [f"{days + 1} sets of clothes", "toiletries", "phone charger"]

    if high_c >= 30:
        items += ["light clothes", "sunscreen", "sunglasses"]
    if low_c <= 15:
        items += ["warm jacket", "thermal layer"]
    if "rain" in conditions or "showers" in conditions:
        items += ["umbrella", "quick-dry footwear"]
    if "snow" in conditions:
        items += ["gloves", "woollen cap", "waterproof boots"]

    return items


@tool
def estimate_trip_cost(city: str, days: int, travellers: int = 1) -> dict:
    """Estimate a trip cost in Indian rupees."""
    stay_per_night = {
        "goa": 3500,
        "bangalore": 3000,
        "jaipur": 2500,
        "manali": 2800,
    }
    stay = stay_per_night.get(city.lower(), 3000) * days
    food = 1200 * days * travellers
    local_travel = 800 * days

    return {
        "stay_inr": stay,
        "food_inr": food,
        "local_travel_inr": local_travel,
        "total_inr": stay + food + local_travel,
    }


def main() -> None:
    agent = Agent(
        model=BedrockModel(model_id=MODEL_ID),
        tools=[get_weather_forecast, suggest_packing_list, estimate_trip_cost, calculator],
        system_prompt=(
            "You are a practical travel assistant. Check the weather, suggest packing, "
            "estimate cost, and say whether the trip fits the budget."
        ),
    )

    question = " ".join(sys.argv[1:])
    if not question:
        question = (
            "I am going to Goa for 3 days with 2 friends. My budget is 20000 rupees. "
            "What should I pack, and does it fit my budget?"
        )

    print(agent(question))


if __name__ == "__main__":
    main()
