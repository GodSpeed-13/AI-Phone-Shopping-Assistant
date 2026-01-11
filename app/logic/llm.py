from app.logic.llm_client import get_llm_client

client = get_llm_client(provider="groq")

def generate_response(user_query, items):
    """
    items:
    - recommendation → list of phone dicts
    - comparison → list of comparison dicts
    """

    # Detect comparison mode
    is_comparison = "compare" in user_query.lower() and len(items) > 1

    if is_comparison:
        content = "\n".join(
            f"- {p['brand']} {p['model']} | Camera: {p['camera']} | Battery: {p['battery']} | Price: ₹{p['price']}"
            for p in items
        )

        prompt = f"""
You are a mobile shopping assistant.

User query:
{user_query}

Phone comparison data:
{content}

Instructions:
- Analyse user query and data.
- Answer only on the basis of the data provided.
- Write a short comparison summary.
- Mention key differences.
- Return JSON ONLY.
- Strictly Do not answer questions that you think are outside mobile phone domain.

JSON format:
{{
  "message": string,
  "reasons": [string]
}}
"""
    else:
        content = "\n".join(
            f"- {p['brand']} {p['model']} | Camera: {p['camera']} | Battery: {p['battery']} | Price: ₹{p['price']} | Processor: {p.get('processor', 'N/A')} | Features: {', '.join(p.get('features', []))} | Storage: {p.get('storage', 'N/A')} | RAM: {p.get('ram', 'N/A')} | Display: {p.get('display', 'N/A')} | Charging: {p.get('charging', 'N/A')}"
            for p in items
        )

        prompt = f"""
You are a mobile shopping assistant.

User query:
{user_query}

Candidate phones:
{content}

Instructions:
- Analyse user query and data.
- Answer only on the basis of the data provided.
- Write a friendly intro.
- Give one reason per phone.
- Do NOT invent specs.
- Return JSON ONLY.
- Strictly Do not answer questions that you think are outside mobile phone domain.

JSON format:
{{
  "message": string,
  "reasons": [string]
}}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        response_format={"type": "json_object"},
    )

    return response.choices[0].message.content
