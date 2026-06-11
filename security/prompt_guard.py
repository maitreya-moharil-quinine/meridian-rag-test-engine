BLOCKED_PATTERNS = [
    "ignore previous instructions",
    "reveal system prompt",
    "show api key",
    "bypass security",
    "developer instructions"
]

def detect_prompt_injection(question: str):
    question = question.lower()

    for pattern in BLOCKED_PATTERNS:
        if pattern in question:
            return True

    return False
