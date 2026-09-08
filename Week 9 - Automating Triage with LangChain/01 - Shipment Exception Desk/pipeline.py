# What this file does: routes one exception report from raw text to a finished outcome.
"""The core exercise: chains for language, plain Python for the business rules."""

from chains import CATEGORIES, classify_chain, draft_email_chain, escalate_chain
from tools import (
    calculate_damage_compensation,
    calculate_delay_compensation,
    calculate_lost_compensation,
    read_damage_percent,
    read_days_late,
)


# Premium customers reach a human sooner, so their threshold is the lower one.
ESCALATION_THRESHOLDS = {
    "premium": 250.0,
    "standard": 500.0,
}


def classify(report: str) -> str:
    """Ask the chain for a category and keep it inside the four we can route."""
    answer = classify_chain.invoke({"report": report}).strip().lower()

    # The model returns one word, but a stray sentence should still route safely.
    for category in CATEGORIES:
        if category in answer:
            return category

    return "unknown"


def compensate(category: str, report: str, shipment_value: float) -> dict:
    """Send the report to the calculator that matches its category."""
    if category == "delayed":
        return calculate_delay_compensation(shipment_value, read_days_late(report))

    if category == "damaged":
        return calculate_damage_compensation(shipment_value, read_damage_percent(report))

    if category == "lost":
        return calculate_lost_compensation(shipment_value)

    # An unclassified report has no policy to price, so it is worth nothing yet.
    return {"category": "unknown", "compensation": 0.0, "rule": "no policy matched"}


def escalation_reason(category: str, compensation: float, customer_tier: str) -> str:
    """Return why this exception needs a human, or an empty string if it does not."""
    if category == "unknown":
        return "The report could not be classified, so a human must read it."

    threshold = ESCALATION_THRESHOLDS[customer_tier]

    if compensation > threshold:
        return (
            f"Compensation ${compensation:,.2f} is over the ${threshold:,.0f} "
            f"limit for {customer_tier} customers."
        )

    return ""


def process_exception(
    report: str, shipment_value: float, customer_tier: str = "standard"
) -> dict:
    """Classify, price, and either escalate to a manager or answer the customer."""
    steps = []

    category = classify(report)
    steps.append(f"Classified as: {category}")

    priced = compensate(category, report, shipment_value)
    compensation = priced["compensation"]
    steps.append(f"Applied rule: {priced['rule']}")
    steps.append(f"Compensation: ${compensation:,.2f}")

    reason = escalation_reason(category, compensation, customer_tier)

    if reason:
        steps.append(f"Escalated: {reason}")
        message = escalate_chain.invoke(
            {
                "category": category,
                "shipment_value": f"{shipment_value:,.2f}",
                "customer_tier": customer_tier,
                "compensation": f"{compensation:,.2f}",
                "reason": reason,
                "report": report,
            }
        )
    else:
        steps.append("Auto-resolved: within the limit for this customer tier.")
        message = draft_email_chain.invoke(
            {
                "category": category,
                "compensation": f"{compensation:,.2f}",
                "customer_tier": customer_tier,
                "report": report,
            }
        )

    return {
        "report": report,
        "category": category,
        "shipment_value": shipment_value,
        "customer_tier": customer_tier,
        "compensation": compensation,
        "escalated": bool(reason),
        "reason": reason,
        "message": message,
        "steps": steps,
    }
