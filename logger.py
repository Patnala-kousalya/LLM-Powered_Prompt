import os
import json
import time

LOG_PATH = os.path.join(os.path.dirname(__file__), "route_log.jsonl")

def log_route(routed_intent, confidence, user_message, final_response, classifier_intent=None):
    entry = {
        "timestamp": time.time(),
        "intent": routed_intent,
        "confidence": confidence,
        "user_message": user_message,
        "final_response": final_response,
    }
    if classifier_intent is not None:
        entry["classifier_intent"] = classifier_intent

    # Append line-delimited JSON (creates file if missing)
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
