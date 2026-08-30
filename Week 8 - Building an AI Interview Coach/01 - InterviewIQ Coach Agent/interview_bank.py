# What this file does: stores the interview questions and the keywords a good answer should cover.
"""Sample interview questions used by the coach agent."""

QUESTIONS = [
    {
        "id": "teamwork-conflict",
        "category": "behavioral",
        "question": (
            "Tell me about a time you disagreed with a teammate. "
            "How did you handle it?"
        ),
        "expected_keywords": [
            "disagree",
            "listen",
            "perspective",
            "compromise",
            "resolve",
            "outcome",
        ],
    },
    {
        "id": "missed-deadline",
        "category": "behavioral",
        "question": "Describe a project where you missed a deadline. What happened?",
        "expected_keywords": [
            "deadline",
            "cause",
            "communicat",
            "stakeholders",
            "recover",
            "learn",
        ],
    },
    {
        "id": "debug-production",
        "category": "technical",
        "question": (
            "Walk me through how you would debug a service that is returning "
            "500 errors in production."
        ),
        "expected_keywords": [
            "logs",
            "reproduce",
            "monitoring",
            "rollback",
            "root cause",
            "fix",
        ],
    },
    {
        "id": "explain-api",
        "category": "technical",
        "question": "How would you explain a REST API to a non-technical stakeholder?",
        "expected_keywords": [
            "request",
            "response",
            "analogy",
            "endpoint",
            "data",
            "simple",
        ],
    },
    {
        "id": "competing-priorities",
        "category": "situational",
        "question": (
            "Two managers give you urgent work on the same afternoon. "
            "What do you do?"
        ),
        "expected_keywords": [
            "clarify",
            "priority",
            "impact",
            "negotiat",
            "communicat",
            "deliver",
        ],
    },
]

# Lookup index so the app and the test harnesses can fetch one question directly.
QUESTIONS_BY_ID = {question["id"]: question for question in QUESTIONS}
