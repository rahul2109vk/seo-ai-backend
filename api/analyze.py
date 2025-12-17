import json
import os
import requests
from bs4 import BeautifulSoup
from openai import OpenAI

def handler(request):
    try:
        # Safely parse body (Vercel-compatible)
        body = request.get("body")
        if body:
            data = json.loads(body)
        else:
            data = {}

        url = data.get("url")

        if not url:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "URL is required"})
            }

        # Fetch webpage
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        title = soup.title.string if soup.title else ""
        meta = soup.find("meta", attrs={"name": "description"})
        meta_desc = meta["content"] if meta else ""

        # Create OpenAI client INSIDE handler
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

        prompt = f"""
        Analyze this webpage SEO:
        Title: {title}
        Meta description: {meta_desc}
        URL: {url}

        Give SEO improvements.
        """

        ai_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
