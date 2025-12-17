@app.post("/analyze-site")
def analyze_site(data: SiteRequest):
    import os
    from openai import OpenAI

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY missing")

    client = OpenAI(api_key=api_key)

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
Title: {title}
Meta description: {meta_desc}
H1s: {h1s}

Return:
- site category
- missing pages
- 5 competitors
- SEO improvements
(JSON only)
"""

    ai_response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return {
        "domain": domain,
        "title": title,
        "meta_description": meta_desc,
        "h1s": h1s,
        "analysis": ai_response.choices[0].message.content
    }
