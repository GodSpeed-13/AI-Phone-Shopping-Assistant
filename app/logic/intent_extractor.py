import json
from app.logic.llm_client import get_llm_client

client = get_llm_client(provider="groq")


def extract_intent(question: str) -> dict:
    prompt = f"""
You are an intent extraction engine for a mobile shopping assistant.

Extract structured intent from the user question.

Return JSON ONLY. No explanations.

Rules:
- budget must be a number (in INR) or null.
- brands must be a list (empty list if none mentioned).
- use_cases must be a list chosen ONLY from:
  camera, battery, gaming, performance, compact, display, software, water resistance, value for money, flagship, budget, photography, video, social media, multitasking, everyday use, durability, design, audio, 5G, fast charging, wireless charging, storage, ram, processor, special features.
- comparison must be true or false.
- max_results must be an integer between 1 and 3.
- For recommendation queries (best, suggest, recommend), set max_results to 3.
- For comparison queries, set max_results to 2.
- For very specific queries, set max_results to 1.
- Do NOT invent brands or values.
- If unsure, return null or empty list.

JSON schema:
{{
  "budget": number | null,
  "brands": [string],
  "use_cases": [string],
  "comparison": boolean,
  "max_results": number
}}

Question:
{question}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        response_format={"type": "json_object"},
    )

    intent = json.loads(response.choices[0].message.content)

    # ---------- Hard validation / normalization ----------
    intent.setdefault("budget", None)
    intent.setdefault("brands", [])
    intent.setdefault("use_cases", [])
    intent.setdefault("comparison", False)
    intent.setdefault("max_results", 1)

    if not isinstance(intent["brands"], list):
        intent["brands"] = [intent["brands"]]

    if not isinstance(intent["use_cases"], list):
        intent["use_cases"] = [intent["use_cases"]]

    if intent["max_results"] < 1:
        intent["max_results"] = 1
    if intent["max_results"] > 3:
        intent["max_results"] = 3

    return intent


if __name__ == "__main__":
    tests = [
        "Best camera phone under 30000",
        "Compare Samsung and Pixel phones for photography",
        "Suggest a compact phone with good battery life",
        "Gaming phone below 25000",
        "Which phone has the best display?"
    ]

    for q in tests:
        print("\nQ:", q)
        print(extract_intent(q))
