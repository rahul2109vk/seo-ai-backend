import json
import os
import requests
from bs4 import BeautifulSoup
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def handler(request):
    try:
        body = json.loads(request.body)
        url = body.get("url")

        if not url:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "URL is required"})
            }

        html = requests.get(url, timeout=10).text
        soup = BeautifulSoup(html, "html.parser")

        title = soup.title.string if soup.title else ""
        meta = soup.find("meta", attrs={"name": "description"})
        meta_desc = meta["content"] if meta else ""

        prompt = f"""
        Analyze this webpage SEO:
        Title: {title}
        Meta description: {meta_desc}
        URL: {url}

        Give SEO improvements.
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        return {
            "statusCode": 200,
            "body": json.dumps({
                "title": title,
                "meta_description": meta_desc,
                "seo_suggestions": response.choices[0].message.content
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
