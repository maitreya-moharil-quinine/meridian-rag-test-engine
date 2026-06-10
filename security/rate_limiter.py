from datetime import datetime, timedelta

REQUESTS = {}

MAX_REQUESTS = 5
WINDOW_SECONDS = 60


def is_rate_limited(client_id: str):

    now = datetime.now()

    if client_id not in REQUESTS:
        REQUESTS[client_id] = []

    REQUESTS[client_id] = [
        ts
        for ts in REQUESTS[client_id]
        if now - ts < timedelta(seconds=WINDOW_SECONDS)
    ]

    if len(REQUESTS[client_id]) >= MAX_REQUESTS:
        return True

    REQUESTS[client_id].append(now)

    return False