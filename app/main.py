from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

import requests

from app.circuit_breaker import CircuitBreaker

app = FastAPI()

breaker = CircuitBreaker()

@app.middleware("http")
async def add_student_id(request: Request, call_next):

    response = await call_next(request)

    response.headers["X-Student-ID"] = "BSAI23037"

    return response

@app.get("/")
def home():

    return {
        "message": "StudySync Backend Running"
    }

@app.get("/health")
def health():

    return {
        "status": "healthy"
    }

@app.get("/circuit-status")
def circuit_status():

    return {
        "state": breaker.state,
        "failures": breaker.failure_count
    }

@app.get("/ask-ai")
def ask_ai(bypass: bool = False):

    if not bypass and not breaker.can_call():

        return {
            "message": "Fallback: AI service temporarily unavailable"
        }

    try:

        response = requests.get(
            "http://127.0.0.1:9000/llm",
            timeout=3
        )

        if not bypass:
            breaker.reset()

        return {
            "data": response.json()
        }

    except Exception:

        if not bypass:
            breaker.record_failure()

        return JSONResponse(
            status_code=503,
            content={
                "message": "LLM failed. Circuit breaker activated." if not bypass else "LLM failed (Timeout)."
            }
        )