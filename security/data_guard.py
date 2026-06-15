SENSITIVE_TERMS = [
    "api key",
    "password",
    "secret",
    "token",
    "credentials"
]

def contains_sensitive_request(question: str):

    question = question.lower()

    for term in SENSITIVE_TERMS:
        if term in question:
            return True

    return False
