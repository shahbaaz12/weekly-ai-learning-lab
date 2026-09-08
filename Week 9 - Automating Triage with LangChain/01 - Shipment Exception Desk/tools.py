# What this file does: the compensation rules. Plain Python, no LLM call anywhere in here.
"""Northwind's compensation policy, written as three calculators.

The assignment does not state the policy, so these numbers are this project's
own. Change them in one place here and every route picks up the new rule.
"""

import re


# Delay: a daily rate on the shipment value, floored so a small claim is worth
# paying, and capped so a long delay never costs more than a quarter of the load.
DELAY_RATE_PER_DAY = 0.02
DELAY_MINIMUM = 10.0
DELAY_CAP_FRACTION = 0.25

# Damage: pay the share of the shipment that was actually damaged.
DAMAGE_MINIMUM = 25.0

# Lost: the whole shipment, plus a service credit for the disruption.
LOST_SERVICE_CREDIT = 0.10

# Used when the report describes damage in words instead of a percentage.
DAMAGE_WORDS = {
    "scuff": 10,
    "scratch": 10,
    "minor": 10,
    "dented": 30,
    "torn": 30,
    "soaked": 60,
    "crushed": 80,
    "destroyed": 100,
    "severe": 80,
}
DEFAULT_DAMAGE_PERCENT = 30


def read_days_late(report: str) -> int:
    """Pull the number of days late out of the report text, defaulting to one."""
    match = re.search(r"(\d+)\s*day", report.lower())
    return int(match.group(1)) if match else 1


def read_damage_percent(report: str) -> int:
    """Pull a damage percentage out of the report, by number or by describing word."""
    text = report.lower()
    match = re.search(r"(\d+)\s*%", text)

    if match:
        return min(int(match.group(1)), 100)

    for word, percent in DAMAGE_WORDS.items():
        if word in text:
            return percent

    return DEFAULT_DAMAGE_PERCENT


def calculate_delay_compensation(shipment_value: float, days_late: int) -> dict:
    """Pay a daily rate for a late shipment, floored and capped."""
    raw = shipment_value * DELAY_RATE_PER_DAY * days_late
    capped = min(max(raw, DELAY_MINIMUM), shipment_value * DELAY_CAP_FRACTION)

    return {
        "category": "delayed",
        "compensation": round(capped, 2),
        "days_late": days_late,
        "rule": f"{DELAY_RATE_PER_DAY:.0%} of value per day, capped at "
        f"{DELAY_CAP_FRACTION:.0%} of value",
    }


def calculate_damage_compensation(shipment_value: float, damage_percent: int) -> dict:
    """Pay the damaged share of the shipment value."""
    raw = shipment_value * damage_percent / 100

    return {
        "category": "damaged",
        "compensation": round(max(raw, DAMAGE_MINIMUM), 2),
        "damage_percent": damage_percent,
        "rule": f"{damage_percent}% of value, minimum ${DAMAGE_MINIMUM:.0f}",
    }


def calculate_lost_compensation(shipment_value: float) -> dict:
    """Pay the full shipment value plus a service credit."""
    credit = shipment_value * LOST_SERVICE_CREDIT

    return {
        "category": "lost",
        "compensation": round(shipment_value + credit, 2),
        "service_credit": round(credit, 2),
        "rule": f"full value plus a {LOST_SERVICE_CREDIT:.0%} service credit",
    }
