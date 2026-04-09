import json
from datetime import datetime

LOG_FILE = "data/logs.json"


def log_feedback(input_data, tf_code, suggestions, action):
    entry = {
        "timestamp": str(datetime.now()),
        "input": input_data,
        "terraform": tf_code,
        "suggestions": suggestions,
        "action": action
    }

    try:
        with open(LOG_FILE, "r") as f:
            data = json.load(f)
    except:
        data = []

    data.append(entry)

    with open(LOG_FILE, "w") as f:
        json.dump(data, f, indent=2)