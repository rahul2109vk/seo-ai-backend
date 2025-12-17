from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup
import os
import openai

# Configure OpenAI (old stable SDK)
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

class URLInput(BaseModel):
    url: str

@app.get("/")
def home():
    return {"status": "SEO AI Backend running (stable)"}

@app.get("/health")
def health():
    return {"health": "ok"}

def crawl_page(url):
    try:
        r = requests.get(
            url,
            timeout=10,
            headers={"User-Agent": "Mozilla/5.0"}
        )
        soup = BeautifulSoup(r.text, "html.parser")

        title = soup.title.string if soup.title else ""
        h1 = soup.find("h1").get_text() if soup.find("h1") else ""
        text = soup.get_text(separator=" ", strip=True)

        return title, h1, text[:4000]
    except Exception:
        return "", "", ""

def ask_ai(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"AI error: {str(e)}"

@app.post("/site-audit")
def site_audit(data: URLInput):
    if not data.url.startswith("http"):
        raise HTTPException(status_code=400, detail="Invalid URL")

    title, h1, content = crawl_page(data.url)

    prompt = f"""
    You are an SEO expert.

    Website URL: {data.url}
    Page Title: {title}
    H1: {h1}

    Page Content:
    {content}

    Tasks:
    - Identify website niche
    - Suggest competitors
    - Optimize meta title, description, and H1
    - Suggest top pages to optimize
