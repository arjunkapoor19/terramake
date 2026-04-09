import json

LOG_FILE = "data/logs.json"


def analyze_feedback():
    try:
        with open(LOG_FILE, "r") as f:
            data = json.load(f)
    except:
        return "No logs found"

    if not data:
        return "No feedback data yet"

    total = len(data)
    accepted = sum(1 for d in data if d["action"] == "accept")
    rejected = sum(1 for d in data if d["action"] == "reject")

    acceptance_rate = (accepted / total) * 100 if total > 0 else 0

    return {
        "total": total,
        "accepted": accepted,
        "rejected": rejected,
        "acceptance_rate": round(acceptance_rate, 2)
    }

def get_rejected_patterns():
    try:
        with open(LOG_FILE, "r") as f:
            data = json.load(f)
    except:
        return []

    rejected = [d["suggestions"] for d in data if d["action"] == "reject"]

    return rejected