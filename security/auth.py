from fastapi import Header, HTTPException

SECRET_API_KEY = "1234567890"

def verify_api_key(
    x_api_key: str = Header(None)
):

    if x_api_key != SECRET_API_KEY:

        raise HTTPException(
            status_code=401,
            detail="Unauthorized"
        )

    return True
