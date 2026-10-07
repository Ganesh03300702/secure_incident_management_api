from fastapi import Header, HTTPException

DEMO_TOKEN = "demo-cisco-project-token"

def require_token(authorization: str | None = Header(default=None)):
    if authorization != f"Bearer {DEMO_TOKEN}":
        raise HTTPException(status_code=401, detail="Invalid or missing authentication token")
