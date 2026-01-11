def compare_phones(phones):
    comparison_data = []

    for p in phones:
        comparison_data.append({
            "brand": p["brand"],
            "model": p["model"],
            "camera": p["camera"],
            "battery": p["battery"],
            "price": p["price"],
            "processor": p.get("processor", "")
        })

    return comparison_data
