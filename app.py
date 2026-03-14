"""CLI entrypoint for the LLM Prompt Router.

This file provides a thin CLI wrapper that imports the classifier and
router implementations from dedicated modules so the project exposes a
clean programmatic API for tests and the interactive CLI.
"""

from typing import Dict
import sys

from classifier import classify_intent
from router import route_and_respond


def _interactive():
    print("LLM Prompt Router CLI")
    print("Type 'exit' to quit.")
    try:
        while True:
            user_msg = input("\nUser: ").strip()
            if not user_msg:
                continue
            if user_msg.lower() in ("exit", "quit"):
                break

            intent = classify_intent(user_msg)
            label = intent.get("intent", "unclear")
            conf = float(intent.get("confidence", 0.0))
            print(f"Detected Intent: {label} ({conf:.2f})\n")

            response = route_and_respond(user_msg, intent)
            print("Response:\n" + response)
    except (KeyboardInterrupt, EOFError):
        print()

    print("Goodbye.")


def _cli_args_mode(args):
    user_msg = " ".join(args)
    intent = classify_intent(user_msg)
    label = intent.get("intent", "unclear")
    conf = float(intent.get("confidence", 0.0))
    print(f"Detected Intent: {label} ({conf:.2f})")
    out = route_and_respond(user_msg, intent)
    print("\nResponse:\n", out)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        _cli_args_mode(sys.argv[1:])
    else:
        _interactive()
