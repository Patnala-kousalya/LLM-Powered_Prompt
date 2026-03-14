from app import classify_intent, route_and_respond
from llm_client import OPENAI_API_KEY

TEST_MESSAGES = [
    "how do i sort a list of objects in python?",
    "explain this sql query",
    "This paragraph sounds awkward",
    "I'm preparing for a job interview",
    "what's the average of these numbers: 12 45 23 67",
    "Help me make this better",
    "hey",
    "Can you write me a poem about clouds?",
    "Rewrite this sentence to be more professional",
    "what is a pivot table",
    "fix this bug: for i in range(10) print(i)",
    "How do I structure a cover letter?",
    "My boss says my writing is too verbose",
    "Can you explain how a for loop works in Python?",
    "Give me some career advice for a junior developer."
]


def run_tests():
    simulated = OPENAI_API_KEY is None

    for m in TEST_MESSAGES:
        if simulated:
            # Lightweight heuristic for offline testing to exercise routing
            low = {"intent": "unclear", "confidence": 0.0}
            text = m.lower()
            if any(k in text for k in ("sort", "python", "bug", "for i in", "print(")):
                intent = {"intent": "code", "confidence": 0.95}
            elif any(k in text for k in ("sql", "pivot", "average", "numbers", "data")):
                intent = {"intent": "data", "confidence": 0.9}
            elif any(k in text for k in ("resume", "interview", "career", "cover letter")):
                intent = {"intent": "career", "confidence": 0.92}
            elif any(k in text for k in ("rewrite", "paragraph", "writing", "professional", "verbose", "poem")):
                intent = {"intent": "writing", "confidence": 0.9}
            else:
                intent = low
        else:
            intent = classify_intent(m)

        resp = route_and_respond(m, intent)
        print("---")
        print("MSG:", m)
        print("INTENT:", intent)
        print("RESP:\n", resp)


if __name__ == "__main__":
    run_tests()
