from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"status": "Backend is running"}

@app.get("/health")
def health():
    return {"health": "ok"}
