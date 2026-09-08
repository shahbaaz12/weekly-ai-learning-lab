# What this file does: runs the triage desk in the terminal, for quick testing while building.

import sys

from session import TriageSession


TIERS = ("standard", "premium")


def ask_tier() -> str:
    """Read a customer tier, defaulting to standard on a blank line."""
    tier = input("Customer tier (standard/premium): ").strip().lower()
    return tier if tier in TIERS else "standard"


def main() -> None:
    # The drafted messages contain characters a Windows terminal cannot print by default.
    sys.stdout.reconfigure(encoding="utf-8")

    session = TriageSession()
    print("Shipment Exception Desk. Type 'quit' at the report to stop.\n")

    while True:
        report = input("Exception report: ").strip()

        if report.lower() in {"quit", "exit"}:
            break

        if not report:
            continue

        shipment_value = float(input("Shipment value in dollars: ").strip() or 0)
        outcome = session.handle(report, shipment_value, ask_tier())

        print("\nSteps:")
        for step in outcome["steps"]:
            print(f"- {step}")

        heading = "Manager note" if outcome["escalated"] else "Customer email"
        print(f"\n{heading}:\n{outcome['message']}\n")

    if not session.processed:
        print("No exceptions handled, so there is no summary.")
        return

    print("\n" + session.generate_daily_summary())


if __name__ == "__main__":
    main()
