SENSITIVE_TERMS = [
    "api key",
    "apikey",
    "password",
    "secret",
    "token",
    "employee details",
    "employee address",
    "salary",
    "credentials"
]

def contains_sensitive_request(question: str):

    question = question.lower()

    for term in SENSITIVE_TERMS:
        if term in question:
            return True

    return False
