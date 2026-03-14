import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    # Clear message for users when the key is missing
    print("OPENAI_API_KEY not found. Please create a .env file with OPENAI_API_KEY=your_key")

# Initialize OpenAI client when available
client = None
if OPENAI_API_KEY:
    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
    except Exception:
        client = None


def call_chat_model(messages, model=None, temperature=0.0, max_tokens=500):
    """Call the OpenAI chat completions endpoint using the new OpenAI client.

    Raises RuntimeError if the API key/client is not configured.
    Returns the assistant content string on success.
    """
    if not client:
        raise RuntimeError("OPENAI_API_KEY not set or OpenAI client not initialized")

    model = model or os.getenv("LLM_MODEL", "gpt-3.5-turbo")
    resp = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )

    # Resp is usually a dict-like object with choices
    try:
        return resp["choices"][0]["message"]["content"]
    except Exception:
        # Fallback: try attribute access
        try:
            return resp.choices[0].message.content
        except Exception:
            raise RuntimeError("Unexpected response shape from OpenAI client")
