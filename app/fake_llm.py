from fastapi import FastAPI

import time

app = FastAPI()

@app.get("/llm")
def fake_llm():

    time.sleep(60)

    return {
        "response": "AI Response"
    }