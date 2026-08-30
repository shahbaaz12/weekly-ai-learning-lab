# What this file does: runs the whole interview in the terminal, for quick testing while building.

import sys

from agent import InterviewCoach
from interview_bank import QUESTIONS


def main() -> None:
    # Let Windows terminals print all characters returned by the model.
    sys.stdout.reconfigure(encoding="utf-8")

    coach = InterviewCoach()
    print("InterviewIQ. Type 'skip' to jump a question, or 'quit' to stop early.\n")

    for number, question in enumerate(QUESTIONS, start=1):
        print(f"--- Question {number} of {len(QUESTIONS)} ({question['category']}) ---")
        print(question["question"])
        answer = input("\nYour answer: ").strip()

        if answer.lower() == "quit":
            break

        if answer.lower() == "skip" or not answer:
            print("Skipped.\n")
            continue

        print("\nEvaluating...\n")
        print(coach.evaluate_answer(question, answer))

        summary = coach.session_summary()
        print(f"\n(Average so far: {summary['average_relevance']}/100)\n")

    if not coach.evaluations:
        print("No answers given, so there is no report.")
        return

    # Show that meta-questions work from the whole session, not just the last turn.
    print("\n--- Asking the coach a meta-question ---")
    print(coach.ask_agent("What is my weakest area so far?"))

    print("\n" + coach.generate_final_report())


if __name__ == "__main__":
    main()
