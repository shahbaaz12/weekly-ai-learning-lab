# What this file does: the browser interface. All coaching logic stays in agent.py.

import gradio as gr

from agent import InterviewCoach
from interview_bank import QUESTIONS


SCORECARD_HEADERS = ["Question", "Category", "Relevance", "Fillers", "STAR missing"]
SCORECARD_WIDTHS = ["38%", "16%", "16%", "12%", "18%"]

# The panel is narrow, so long questions are shortened for display only.
MAX_QUESTION_CHARACTERS = 55


def scorecard_view(coach) -> list[list]:
    """Return the scorecard rows with the question text trimmed to fit."""
    rows = coach.scorecard_rows()

    for row in rows:
        if len(row[0]) > MAX_QUESTION_CHARACTERS:
            row[0] = row[0][:MAX_QUESTION_CHARACTERS] + "..."

    return rows


def question_markdown(index: int) -> str:
    """Describe the question the candidate is on, or say the interview is over."""
    if index >= len(QUESTIONS):
        return "### Interview complete\n\nPull the final report below."

    question = QUESTIONS[index]
    return (
        f"### Question {index + 1} of {len(QUESTIONS)} "
        f"({question['category']})\n\n{question['question']}"
    )


def submit_answer(answer: str, index: int, coach):
    """Evaluate one answer, update the scorecard, and move to the next question."""
    # The coach is created on the first answer and then kept in the session state.
    coach = coach or InterviewCoach()
    answer = answer.strip()

    if index >= len(QUESTIONS):
        feedback = "The interview is finished. Pull the final report below."
        return feedback, scorecard_view(coach), coach, index, question_markdown(index), ""

    if not answer:
        feedback = "Type an answer before submitting."
        return feedback, scorecard_view(coach), coach, index, question_markdown(index), answer

    feedback = coach.evaluate_answer(QUESTIONS[index], answer)
    index += 1

    return feedback, scorecard_view(coach), coach, index, question_markdown(index), ""


def ask_coach(meta_question: str, coach) -> str:
    """Answer a meta-question using the whole session, mid-interview."""
    if coach is None:
        return "No answers yet. Answer one question and I can tell you how it is going."

    meta_question = meta_question.strip()

    if not meta_question:
        return "Type a question for the coach."

    return coach.ask_agent(meta_question)


def pull_report(coach) -> str:
    """Return the aggregated final report."""
    if coach is None:
        return "No answers yet, so there is nothing to report."

    return coach.generate_final_report()


with gr.Blocks(title="InterviewIQ") as demo:
    # Each browser session gets its own coach and its own place in the question list.
    coach_state = gr.State(None)
    index_state = gr.State(0)

    gr.Markdown("# InterviewIQ")
    gr.Markdown("A mock-interview coach that scores your answers and remembers the session.")

    with gr.Row():
        with gr.Column(scale=3):
            question_box = gr.Markdown(question_markdown(0))
            answer_box = gr.Textbox(
                label="Your answer",
                placeholder="Answer as if you were speaking to the interviewer...",
                lines=6,
            )
            submit_button = gr.Button("Submit answer", variant="primary")
            feedback_box = gr.Markdown(label="Feedback")

        with gr.Column(scale=2):
            gr.Markdown("## Scorecard")
            scorecard = gr.Dataframe(
                headers=SCORECARD_HEADERS,
                value=[],
                column_widths=SCORECARD_WIDTHS,
                interactive=False,
                wrap=True,
            )

    gr.Markdown("## Ask the coach")
    gr.Markdown("Works at any point, not only at the end.")

    with gr.Row():
        meta_box = gr.Textbox(
            label="Your question",
            placeholder="How am I doing so far? What is my weakest area?",
            scale=3,
        )
        ask_button = gr.Button("Ask", scale=1)

    meta_answer = gr.Markdown()

    report_button = gr.Button("Generate final report", variant="primary")
    report_box = gr.Markdown()

    # Connect each control to the Python function it should run.
    submit_button.click(
        fn=submit_answer,
        inputs=[answer_box, index_state, coach_state],
        outputs=[
            feedback_box,
            scorecard,
            coach_state,
            index_state,
            question_box,
            answer_box,
        ],
    )
    ask_button.click(fn=ask_coach, inputs=[meta_box, coach_state], outputs=meta_answer)
    report_button.click(fn=pull_report, inputs=coach_state, outputs=report_box)


if __name__ == "__main__":
    # Starts a local app. It is not publicly shared.
    demo.launch()
