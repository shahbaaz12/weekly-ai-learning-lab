# What this file does: proves the agent aggregates the whole session instead of only the last turn.
"""Scripted mini-session that verifies session memory and the weakest-area report."""

import sys

from agent import ask_agent, run_turn, session_log
from interview_bank import QUESTIONS_BY_ID


# The weak answer is given FIRST and the strong answer SECOND on purpose.
# An agent that only reads the last turn would name the strong question as the
# weakest area, so this order is what makes the check meaningful.
WEAK_QUESTION_ID = "debug-production"
STRONG_QUESTION_ID = "teamwork-conflict"

WEAK_ANSWER = "Um, I would basically like, you know, just restart it and hope it works."

STRONG_ANSWER = (
    "When I was working on the billing service last year, our team disagreed about "
    "how to handle refunds. I had to get us to one decision before the release. "
    "So I listened to each perspective, wrote both options down, and suggested a "
    "compromise we could test cheaply. As a result we resolved it in one meeting "
    "and the outcome was a refund flow we still use."
)

# Distinctive words from each question, used to see which one the coach names.
WEAK_MARKERS = ("debug", "500", "production")
STRONG_MARKERS = ("disagree", "teammate", "teamwork")


def main() -> None:
    # The model replies contain characters a Windows terminal cannot print by default.
    sys.stdout.reconfigure(encoding="utf-8")

    weak = QUESTIONS_BY_ID[WEAK_QUESTION_ID]
    strong = QUESTIONS_BY_ID[STRONG_QUESTION_ID]

    print("--- Turn 1: the deliberately weak answer ---")
    print(f"Question: {weak['question']}")
    print(run_turn(weak["question"], WEAK_ANSWER, weak["expected_keywords"]))

    print("\n--- Turn 2: the strong answer, given most recently ---")
    print(f"Question: {strong['question']}")
    print(run_turn(strong["question"], STRONG_ANSWER, strong["expected_keywords"]))

    scores = [item["relevance_score"] for item in session_log]
    weakest = min(session_log, key=lambda item: item["relevance_score"])

    print("\n--- Aggregated session ---")
    print(f"Turns remembered: {len(session_log)}")
    print(f"Average relevance: {round(sum(scores) / len(scores), 1)}/100")
    print(f"Weakest question: {weakest['question']}")

    print("\n--- Meta-question asked mid-session ---")
    reply = ask_agent("What is my weakest area so far?")
    print(reply)

    # Check 1: the aggregation itself picked the low-scoring question.
    aggregation_ok = weakest["question"] == weak["question"]

    # Check 2: the coach's own words name the weak question, not the recent one.
    lowered = reply.lower()
    names_weak = any(marker in lowered for marker in WEAK_MARKERS)
    names_strong_only = (
        any(marker in lowered for marker in STRONG_MARKERS) and not names_weak
    )

    print("\n--- Result ---")
    print(f"Aggregation names the weak question  : {aggregation_ok}")
    print(f"Coach's reply names the weak question: {names_weak}")

    if aggregation_ok and names_weak and not names_strong_only:
        print("\nPASS - memory and aggregation use the whole session.")
        return

    print("\nFAIL - the agent is not using the whole session.")

    if not aggregation_ok:
        print(f"  Expected weakest to be: {weak['question']}")
    if not names_weak:
        print("  The reply never named the weak question.")

    sys.exit(1)


if __name__ == "__main__":
    main()
