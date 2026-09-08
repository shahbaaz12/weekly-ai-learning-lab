# What this file does: the browser interface. All triage logic stays in pipeline.py and session.py.

import gradio as gr

from session import TriageSession


LOG_HEADERS = ["#", "Category", "Tier", "Shipment value", "Compensation", "Outcome"]
LOG_WIDTHS = ["6%", "18%", "16%", "22%", "22%", "16%"]


def outcome_markdown(outcome: dict) -> str:
    """Format one processed exception as the outcome panel."""
    steps = "\n".join(f"{number}. {step}" for number, step in enumerate(outcome["steps"], start=1))
    heading = "Manager note" if outcome["escalated"] else "Customer email"
    badge = "ESCALATED" if outcome["escalated"] else "AUTO-RESOLVED"

    return (
        f"### {badge}\n\n"
        f"**Category:** {outcome['category']}  \n"
        f"**Compensation:** ${outcome['compensation']:,.2f}\n\n"
        f"#### Steps it went through\n\n{steps}\n\n"
        f"#### {heading}\n\n{outcome['message']}"
    )


def submit_report(report: str, shipment_value: float, customer_tier: str, session):
    """Process one report, then refresh the outcome panel and the triage log."""
    # The session is created on the first report and then kept in the browser state.
    session = session or TriageSession()
    report = report.strip()

    if not report:
        return "Enter an exception report before submitting.", session.log_rows(), session, report

    outcome = session.handle(report, float(shipment_value or 0), customer_tier)

    return outcome_markdown(outcome), session.log_rows(), session, ""


def pull_summary(session) -> str:
    """Return the aggregated Daily Triage Summary."""
    if session is None:
        return "No exceptions handled yet, so there is nothing to summarise."

    return session.generate_daily_summary()


with gr.Blocks(title="Shipment Exception Desk") as demo:
    # Each browser session gets its own triage log.
    session_state = gr.State(None)

    gr.Markdown("# Shipment Exception Desk")
    gr.Markdown("Northwind Logistics - automated triage for shipment exception reports.")

    with gr.Row():
        with gr.Column(scale=3):
            report_box = gr.Textbox(
                label="Exception report",
                placeholder="Describe what went wrong with the shipment...",
                lines=6,
            )

            with gr.Row():
                value_box = gr.Number(label="Shipment value ($)", value=500)
                tier_box = gr.Radio(
                    label="Customer tier",
                    choices=["standard", "premium"],
                    value="standard",
                )

            submit_button = gr.Button("Process report", variant="primary")
            outcome_box = gr.Markdown()

        with gr.Column(scale=2):
            gr.Markdown("## Daily Triage Log")
            triage_log = gr.Dataframe(
                headers=LOG_HEADERS,
                value=[],
                column_widths=LOG_WIDTHS,
                interactive=False,
                wrap=True,
            )

    summary_button = gr.Button("Generate Daily Summary", variant="primary")
    summary_box = gr.Markdown()

    # Connect each control to the Python function it should run.
    submit_button.click(
        fn=submit_report,
        inputs=[report_box, value_box, tier_box, session_state],
        outputs=[outcome_box, triage_log, session_state, report_box],
    )
    summary_button.click(fn=pull_summary, inputs=session_state, outputs=summary_box)


if __name__ == "__main__":
    # Starts a local app. It is not publicly shared.
    demo.launch()
