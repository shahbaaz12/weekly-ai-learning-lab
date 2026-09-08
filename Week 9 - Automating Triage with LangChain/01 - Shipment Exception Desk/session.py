# What this file does: remembers every exception processed today and aggregates the day's numbers.
"""The Daily Triage Log. Python does the arithmetic, never the model."""

from pipeline import process_exception


class TriageSession:
    """Holds one analyst's working day and summarises it on demand."""

    def __init__(self):
        self.processed = []

    def handle(self, report: str, shipment_value: float, customer_tier: str) -> dict:
        """Run one report through the pipeline and keep the outcome."""
        outcome = process_exception(report, shipment_value, customer_tier)
        self.processed.append(outcome)
        return outcome

    def log_rows(self) -> list[list]:
        """Return one row per exception handled, for the Daily Triage Log."""
        return [
            [
                number,
                item["category"],
                item["customer_tier"],
                f"${item['shipment_value']:,.2f}",
                f"${item['compensation']:,.2f}",
                "escalated" if item["escalated"] else "auto-resolved",
            ]
            for number, item in enumerate(self.processed, start=1)
        ]

    def totals_by_category(self) -> dict:
        """Add up compensation per category, which is what decides the costliest."""
        totals = {}

        for item in self.processed:
            category = item["category"]
            totals[category] = totals.get(category, 0.0) + item["compensation"]

        return totals

    def summary(self) -> dict:
        """Aggregate the day. A category of many small payouts can beat one big one."""
        if not self.processed:
            return {"handled": 0}

        totals = self.totals_by_category()
        escalated = sum(1 for item in self.processed if item["escalated"])
        costliest = max(totals, key=lambda category: totals[category])

        return {
            "handled": len(self.processed),
            "total_compensation": round(
                sum(item["compensation"] for item in self.processed), 2
            ),
            "escalated": escalated,
            "escalation_rate": round(100 * escalated / len(self.processed)),
            "costliest_category": costliest,
            "costliest_total": round(totals[costliest], 2),
            "totals_by_category": totals,
        }

    def generate_daily_summary(self) -> str:
        """Format the aggregated day as the Daily Triage Summary."""
        if not self.processed:
            return "No exceptions handled yet, so there is nothing to summarise."

        report = self.summary()
        lines = [
            "## Daily Triage Summary",
            "",
            f"- **Exceptions handled:** {report['handled']}",
            f"- **Total compensation paid:** ${report['total_compensation']:,.2f}",
            f"- **Escalated:** {report['escalated']} of {report['handled']} "
            f"({report['escalation_rate']}%)",
            f"- **Costliest category:** {report['costliest_category']} "
            f"(${report['costliest_total']:,.2f})",
            "",
            "### Compensation by category",
            "",
        ]

        # Show every category so the costliest one can be checked by eye.
        for category, total in sorted(
            report["totals_by_category"].items(), key=lambda pair: pair[1], reverse=True
        ):
            lines.append(f"- {category}: ${total:,.2f}")

        return "\n".join(lines)
