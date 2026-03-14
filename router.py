import os
from typing import Dict

from prompts import PROMPTS
from llm_client import call_chat_model
from logger import log_route


def route_and_respond(message: str, intent_obj: Dict[str, object]) -> str:
    classifier_intent = intent_obj.get("intent", "unclear")
    classifier_confidence = float(intent_obj.get("confidence", 0.0))

    try:
        threshold = float(os.getenv("CONFIDENCE_THRESHOLD", "0.7"))
    except Exception:
        threshold = 0.7

    routed_intent = classifier_intent if classifier_confidence >= threshold else "unclear"

    if routed_intent == "unclear":
        clarifier = PROMPTS.get("clarify")
        question = clarifier or "Are you asking about coding, data analysis, writing help, or career advice?"
        log_route("unclear", classifier_confidence, message, question, classifier_intent=classifier_intent)
        return question

    system_prompt = PROMPTS.get(routed_intent)
    if not system_prompt:
        final = "I couldn't find an expert for that intent; can you clarify?"
        log_route("unclear", classifier_confidence, message, final, classifier_intent=classifier_intent)
        return final

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": message},
    ]
    try:
        response = call_chat_model(messages, model=os.getenv("RESPONSE_MODEL", "gpt-4o"), temperature=0.2, max_tokens=800)
    except Exception:
        final = "Sorry, I can't reach the LLM service right now."
        log_route(routed_intent, classifier_confidence, message, final, classifier_intent=classifier_intent)
        return final

    log_route(routed_intent, classifier_confidence, message, response, classifier_intent=classifier_intent)
    return response
