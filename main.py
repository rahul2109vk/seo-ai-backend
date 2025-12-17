from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup
import os
from openai import OpenAI

app = FastAPI()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class SiteRequest(BaseModel):
    domain: str

@app.get("/")
def home():
    return {"status": "SEO AI Backend Running"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/analyze-site")
def analyze_site(data: SiteRequest):
    domain = data.domain.strip()

    if not domain.startswith("http"):
        domain = "https://" + domain

    try:
        response = requests.get(domain, timeout=10)
    except Exception:
        raise HTTPException(status_code=400, detail="Website not reachable")

    soup = BeautifulSoup(response.text, "html.parser")

    title = soup.title.string if soup.title else ""
    meta_desc = ""
    meta = soup.find("meta", attrs={"name": "description"})
    if meta and meta.get("content"):
        meta_desc = meta["content"]

    h1s = [h.get_text(strip=True) for h in soup.find_all("h1")]

    prompt = f"""
You are an SEO expert.

Website URL: {domain}
Page titl
