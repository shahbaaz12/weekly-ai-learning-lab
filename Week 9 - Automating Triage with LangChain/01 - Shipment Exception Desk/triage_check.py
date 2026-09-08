# What this file does: feeds four canned reports through the pipeline and checks where each one lands.
"""Scripted check that every category and both escalation branches route correctly."""

import sys

from session import TriageSession


# Each case states the outcome it must reach. The garbled one is the important
# case: it has to escalate on category alone, with no compensation to trigger it.
CASES = [
    {
        "name": "Mild delay, low value, standard tier",
        "report": (
            "Our weekly restock pallet arrived 2 days late. Nothing was damaged, "
            "but the store shelves were empty over the weekend."
        ),
        "shipment_value": 400.0,
        "customer_tier": "standard",
        "expect_category": "delayed",
        "expect_escalated": False,
    },
    {
        "name": "High-value loss, premium tier",
        "report": (
            "The container with our autumn stock never arrived at the depot. "
            "The carrier has confirmed it cannot be traced and considers it lost."
        ),
        "shipment_value": 8000.0,
        "customer_tier": "premium",
        "expect_category": "lost",
        "expect_escalated": True,
    },
    {
        "name": "Minor damage, low value, standard tier",
        "report": (
            "Two cartons arrived with a minor scuff on the outer packaging. "
            "The goods inside are fine and we can still sell them."
        ),
        "shipment_value": 300.0,
        "customer_tier": "standard",
        "expect_category": "damaged",
        "expect_escalated": False,
    },
    {
        "name": "Garbled report, must escalate on category alone",
        "report": "asdkj ??? shipment ###   ... ?? please 000 advise thx",
        "shipment_value": 120.0,
        "customer_tier": "standard",
        "expect_category": "unknown",
        "expect_escalated": True,
    },
]


def main() -> None:
    # The drafted messages contain characters a Windows terminal cannot print by default.
    sys.stdout.reconfigure(encoding="utf-8")

    session = TriageSession()
    failures = []

    for number, case in enumerate(CASES, start=1):
        outcome = session.handle(
            case["report"], case["shipment_value"], case["customer_tier"]
        )
        routed = "escalated" if outcome["escalated"] else "auto-resolved"
        expected = "escalated" if case["expect_escalated"] else "auto-resolved"

        print(f"--- Case {number}: {case['name']} ---")
        print(f"Expected: {case['expect_category']} / {expected}")
        print(f"Actual:   {outcome['category']} / {routed}")
        print(f"Compensation: ${outcome['compensation']:,.2f}")

        if outcome["category"] != case["expect_category"]:
            failures.append(
                f"Case {number} classified as {outcome['category']}, "
                f"expected {case['expect_category']}."
            )

        if outcome["escalated"] != case["expect_escalated"]:
            failures.append(f"Case {number} was {routed}, expected {expected}.")

        print()

    print(session.generate_daily_summary())

    print("\n--- Result ---")

    if not failures:
        print("PASS - all four scenarios landed on their expected outcome.")
        return

    print("FAIL - some scenarios routed incorrectly.")
    for failure in failures:
        print(f"  {failure}")

    sys.exit(1)


if __name__ == "__main__":
    main()
