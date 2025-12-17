from fastapi import FastAPI
import os

app = FastAPI()

@app.get("/")
def home():
    return {"status": "SEO AI Backend Running"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/env-check")
def env_check():
    return {
        "OPENAI_API_KEY": "FOUND" if os.getenv("OPENAI_API_KEY") else "MISSING"
    }
