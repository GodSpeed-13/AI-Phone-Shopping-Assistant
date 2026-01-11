def explain_recommendation(phones):
    if not phones:
        return "No suitable phones found."

    lines = []
    lines.append("Top recommendations:\n")

    for idx, p in enumerate(phones, start=1):
        why = []

        if "camera" in p.get("features", []) or "OIS" in p.get("camera", ""):
            why.append("strong camera capabilities")

        if "5000" in p.get("battery", "") or "5500" in p.get("battery", ""):
            why.append("long battery life")

        if p.get("price", 0) < 30000:
            why.append("great value for money")

        reason = ", ".join(why) if why else "balanced overall performance"

        lines.append(
            f"""{idx}. {p['brand']} {p['model']}
   • Camera: {p['camera']}
   • Battery: {p['battery']}
   • Price: ₹{p['price']}
   • Why: {reason}
"""
        )

    return "\n".join(lines)
