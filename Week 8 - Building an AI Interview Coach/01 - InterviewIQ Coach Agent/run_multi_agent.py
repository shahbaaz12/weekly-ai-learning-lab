# What this file does: runs the bonus two-agent loop - the Interviewer picks, the Evaluator scores.
"""Orchestrator for the optional two-agent mode. The Evaluator in agent.py is unchanged."""

import random
import sys

import agent as evaluator
from interview_bank import QUESTIONS
from interviewer_agent import choose_next_category


# Short on purpose. This is a bonus demo, not the whole question bank.
NUM_TURNS = 3


def group_by_category() -> dict:
    """Group the bank so the Interviewer's chosen category has a pool to draw from."""
    grouped = {}

    for question in QUESTIONS:
        grouped.setdefault(question["category"], []).append(question)

    return grouped


def pick_question(grouped: dict, category: str, asked: set) -> dict:
    """Return an unasked question from the chosen category, or any unasked one."""
    pool = [item for item in grouped.get(category, []) if item["id"] not in asked]

    if not pool:
        pool = [item for item in QUESTIONS if item["id"] not in asked]

    return random.choice(pool) if pool else None


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")

    grouped = group_by_category()
    asked = set()
    summary = ""

    print("InterviewIQ two-agent mode.")
    print("The Interviewer chooses the category, the Evaluator scores the answer.\n")

    for turn in range(1, NUM_TURNS + 1):
        category = choose_next_category(summary)
        question = pick_question(grouped, category, asked)

        if question is None:
            print("No fresh questions left.")
            break

        asked.add(question["id"])

        print(f"--- Turn {turn}: the Interviewer chose '{category}' ---")
        print(question["question"])
        answer = input("Your answer: ").strip()

        if not answer:
            print("Skipped.\n")
            continue

        feedback = evaluator.run_turn(
            question["question"], answer, question["expected_keywords"]
        )
        print(f"\nCoach: {feedback}\n")

        # The Interviewer reads this report before choosing the next category.
        summary = evaluator.generate_final_report()

    print("\n" + evaluator.ask_for_final_report())


if __name__ == "__main__":
    main()
