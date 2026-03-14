import json
import os

PROMPTS_PATH = os.path.join(os.path.dirname(__file__), "prompts.json")
with open(PROMPTS_PATH, "r", encoding="utf-8") as f:
    PROMPTS = json.load(f)

def get_prompt(intent: str) -> str:
    return PROMPTS.get(intent)
