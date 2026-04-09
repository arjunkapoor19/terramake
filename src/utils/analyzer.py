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

def extract_patterns(rejected_list):
    patterns = []

    for r in rejected_list:
        r_lower = r.lower()

        if "public" in r_lower and "s3" in r_lower:
            patterns.append("Avoid making S3 buckets public")

        elif "policy" in r_lower and "principal" in r_lower:
            patterns.append("Avoid overly permissive bucket policies")

        elif "rewrite entire" in r_lower:
            patterns.append("Do not rewrite full resources")

    return list(set(patterns))

