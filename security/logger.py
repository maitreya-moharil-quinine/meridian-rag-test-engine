from datetime import datetime


def log_event(action, question, status):

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    with open(
        "security.log",
        "a"
    ) as f:

        f.write(
            f"[{timestamp}] "
            f"{action} | "
            f"{status} | "
            f"{question}\n"
        )
