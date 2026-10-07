from fastapi import FastAPI
from app.routes import router

app = FastAPI(
    title="Secure Incident Management API",
    version="1.0.0",
    description="REST API for incident management with validation, authentication, logging, and automated testing.",
)

app.include_router(router)

@app.get("/health")
def health():
    return {"status": "healthy"}
