# What this file does: three rule-based tools that measure one interview answer.
"""Evaluation tools. These are plain Python and never call an LLM."""

import re


# Single words are matched on word boundaries so "like" does not match "likely".
FILLER_WORDS = (
    "um",
    "uh",
    "er",
    "like",
    "basically",
    "actually",
    "literally",
    "honestly",
    "you know",
    "i mean",
    "sort of",
    "kind of",
)

# A STAR component counts as present when any of its signal phrases appears.
STAR_SIGNALS = {
    "situation": (
        "when i",
        "we were",
        "at the time",
        "the situation",
        "last year",
        "working on",
        "our team",
        "the project",
    ),
    "task": (
        "i had to",
        "i needed",
        "my job",
        "my role",
        "responsible for",
        "the goal",
        "asked me",
        "my task",
    ),
    "action": (
        "i decided",
        "i built",
        "i created",
        "i implemented",
        "i suggested",
        "i organised",
        "i organized",
        "i reached out",
        "i started",
        "so i",
        "i set up",
    ),
    "result": (
        "as a result",
        "in the end",
        "we shipped",
        "we delivered",
        "the outcome",
        "improved",
        "reduced",
        "increased",
        "we learned",
        "i learned",
        "finally",
    ),
}


def detect_filler_words(answer: str) -> dict:
    """Count filler words such as 'um', 'like', and 'basically' in an answer."""
    text = answer.lower()
    found = {}

    for filler in FILLER_WORDS:
        matches = len(re.findall(rf"\b{re.escape(filler)}\b", text))
        if matches:
            found[filler] = matches

    total_words = len(re.findall(r"\b[\w']+\b", answer))
    filler_count = sum(found.values())

    return {
        "filler_count": filler_count,
        "fillers_found": found,
        "total_words": total_words,
        # An empty answer has no words, so guard the division the UI can trigger.
        "filler_ratio": round(filler_count / total_words, 3) if total_words else 0.0,
    }


def check_star_structure(answer: str) -> dict:
    """Check whether an answer covers Situation, Task, Action, and Result."""
    text = answer.lower()
    present = [
        component
        for component, signals in STAR_SIGNALS.items()
        if any(signal in text for signal in signals)
    ]
    missing = [component for component in STAR_SIGNALS if component not in present]

    return {
        "components_present": present,
        "components_missing": missing,
        "star_complete": not missing,
        "coverage_percent": round(100 * len(present) / len(STAR_SIGNALS)),
    }


def score_relevance(answer: str, expected_keywords: list[str]) -> dict:
    """Score 0-100 by how many of the question's expected keywords appear."""
    text = answer.lower()

    # Substring matching on purpose: the stem "resolve" also matches "resolved".
    matched = [keyword for keyword in expected_keywords if keyword.lower() in text]
    missing = [keyword for keyword in expected_keywords if keyword not in matched]

    return {
        "score": round(100 * len(matched) / len(expected_keywords)),
        "matched_keywords": matched,
        "missing_keywords": missing,
    }
