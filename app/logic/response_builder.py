def build_response(message, phones, reasons):
    recommendations = []

    for idx, p in enumerate(phones):
        reason = reasons[idx] if idx < len(reasons) else "Good overall balance of features"

        recommendations.append({
            "name": f"{p['brand']} {p['model']}",
            "camera": p["camera"],
            "battery": p["battery"],
            "price": f"₹{p['price']}",
            "reason": reason
        })

    return {
        "message": message,
        "intent": "recommendation",
        "recommendations": recommendations,
        "results": phones
    }
