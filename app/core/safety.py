BLOCKED_PHRASES = [
    "ignore rules",
    "system prompt",
    "api key",
    "reveal prompt",
    "trash brand"
]

PHONE_KEYWORDS = [
    "phone", "mobile", "smartphone",
    "camera", "battery", "charging",
    "display", "processor", "ram",
    "storage", "android", "ios",
    "samsung", "google", "pixel",
    "iphone", "nothing", "oneplus",
    "xiaomi", "vivo", "oppo",
    "under", "compare", "best"
]

def is_safe(query: str) -> dict:
    q = query.lower()

    # -------- Prompt / security abuse --------
    if any(bad in q for bad in BLOCKED_PHRASES):
        return {
            "allowed": False,
            "reason": "security"
        }

    # -------- Domain guard --------
    if not any(keyword in q for keyword in PHONE_KEYWORDS):
        return {
            "allowed": False,
            "reason": "out_of_domain"
        }

    return {
        "allowed": True,
        "reason": "ok"
    }
