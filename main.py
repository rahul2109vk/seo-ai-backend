from fastapi import FastAPI
from pydantic import BaseModel
import requests
from bs4 import_toggleSoup
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

class URLInput(BaseModel):
    url: str

def crawl_page(url):
    r = requests.get(url, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")
    text = soup.get_text(separator=" ", strip=True)
    title = soup.title.string if soup.title else ""
    h1 = soup.find("h1").get_text() if soup.find("h1") else ""
    return title, h1, text[:6000]

def ask_ai(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return response.choices[0].message.content

@app.post("/site-audit")
def site_audit(data: URLInput):
    title, h1, content = crawl_page(data.url)

    prompt = f"""
    You are an SEO expert.
    Website URL: {data.url}

    Current Title: {title}
    Current H1: {h1}

    Content:
    {content}

    Tasks:
    1. Identify website niche
    2. Suggest competitors
    3. Optimize meta title, description, and H1
    4. Suggest top pages to optimize
    5. Suggest new pages to create
    """

    result = ask_ai(prompt)
    return {"result": result}
