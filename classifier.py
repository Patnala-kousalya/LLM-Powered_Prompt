import os
import json
from typing import Dict

from llm_client import call_chat_model, OPENAI_API_KEY


CLASSIFIER_PROMPT = (
    "You are an intent classifier. Classify the user's request into one of the following categories:\n\n"
    "code\n"
    "data\n"
    "writing\n"
    "career\n"
    "unclear\n\n"
    "Respond ONLY with valid JSON in this exact format (no other text):\n"
    "{\"intent\": \"label\", \"confidence\": 0.0}"
)


def _safe_parse_json_from_text(text: str):
    try:
        return json.loads(text)
    except Exception:
        return None


def classify_intent(message: str) -> Dict[str, object]:
    """Call LLM to classify intent. Returns {intent:str, confidence:float}.

    If parsing fails or API unavailable returns {'intent':'unclear','confidence':0.0}.
    """
    messages = [
        {"role": "system", "content": CLASSIFIER_PROMPT},
        {"role": "user", "content": message},
    ]

    if not OPENAI_API_KEY:
        return {"intent": "unclear", "confidence": 0.0}

    try:
        content = call_chat_model(messages, model=os.getenv("CLASSIFIER_MODEL", "gpt-3.5-turbo"), temperature=0.0, max_tokens=200)
    except Exception:
        return {"intent": "unclear", "confidence": 0.0}

    parsed = _safe_parse_json_from_text(content)
    if not parsed:
        return {"intent": "unclear", "confidence": 0.0}

    intent = parsed.get("intent")
    confidence = parsed.get("confidence")
    if not isinstance(intent, str) or not isinstance(confidence, (int, float)):
        return {"intent": "unclear", "confidence": 0.0}

    # Ensure confidence is between 0.0 and 1.0
    conf = float(confidence)
    if conf < 0.0 or conf > 1.0:
        conf = max(0.0, min(1.0, conf))

    return {"intent": intent, "confidence": conf}
