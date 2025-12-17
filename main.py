from fastapi import FastAPI
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

class URLInput(BaseModel):
    url: str

def crawl_page(url):
    r = requests.get(url, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")

    title = soup.title.string if soup.title else ""
    h1 = soup.find("h1").get_text() if soup.find("h1") else ""
    text = soup.get_text(separator=" ", strip=True)

    return title, h1, text[:6000]

def ask_ai(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )
    return response.choices[0].message.content

@app.get("/")
def home():
    return {"status": "SEO AI Backend is running"}

@app.post("/site-audit")
def site_audit(data: URLInput):
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
    - Suggest new pages to create
    """

    result = ask_ai(prompt)
    return {"result": result}

