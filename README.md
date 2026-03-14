# LLM Prompt Router

This project implements an intent-based prompt router with two main functions:

- `classify_intent(message: str)` — calls a classifier LLM to return `{intent, confidence}`.
- `route_and_respond(message: str, intent: dict)` — selects a persona prompt and produces a response.

Usage:

1. Set `OPENAI_API_KEY` in your environment (optional; code falls back to 'unclear' behavior if missing).
2. Install dependencies: `pip install -r requirements.txt`.
# LLM Prompt Router

A lightweight intent-based prompt router that classifies user messages and
routes them to specialized persona prompts (code, data, writing, career)
for contextual LLM responses. The project exposes a simple CLI and a
programmatic API for integration and testing.

## Table of contents

- [Features](#features)
- [Architecture](#architecture)
- [Quick start](#quick-start)
- [Usage](#usage)
- [Docker](#docker)
- [Testing](#testing)
- [Prompts & Routing](#prompts--routing)
- [Logging](#logging)
- [Environment variables](#environment-variables)
- [Example inputs](#example-inputs)

## Features

- Intent classification into `code`, `data`, `writing`, `career`, or `unclear`.
- Routing to concise, role-specific system prompts for high-quality replies.
- Interactive CLI and programmatic API (`classify_intent`, `route_and_respond`).
- Line-delimited JSON activity logging to `route_log.jsonl`.
- Docker support for consistent execution environments.

## Architecture

The project is organized into small, focused modules:

- `llm_client.py`: thin OpenAI client wrapper that loads `OPENAI_API_KEY` using `python-dotenv`.
- `classifier.py`: runs the classifier LLM call and returns `{"intent": str, "confidence": float}` with robust parsing.
- `router.py`: maps classifier outputs to persona prompts and calls the LLM for final responses; asks clarifying questions when the intent is unclear.
- `prompts.json` / `prompts.py`: stores and exposes persona system prompts.
- `logger.py`: appends line-delimited JSON entries to `route_log.jsonl` containing intent, confidence, user_message, and final_response.
- `app.py`: CLI entrypoint that wires the pieces together.

## Quick start

1. Create a virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate   # on Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

2. Create a `.env` file in the project root (see `.env.example`):

```text
OPENAI_API_KEY=your_api_key_here
```

3. Run the interactive CLI:

```bash
python app.py
```

Type messages at the prompt. Type `exit` or press Ctrl-C to quit.

## Usage (programmatic)

Import the classifier and router from the project to integrate into other
applications or tests:

```python
from classifier import classify_intent
from router import route_and_respond

intent = classify_intent("how do i sort a list in python?")
response = route_and_respond("how do i sort a list in python?", intent)
```

## Docker

Build and run the CLI inside a container:

```bash
docker build -t prompt-router .
docker run -it --env-file .env prompt-router
# or with docker-compose
docker-compose up --build
```

The CLI will start inside the container and behave the same as local execution.

## Testing

The repository includes `run_tests.py`, which runs a suite of representative
inputs. When `OPENAI_API_KEY` is not set the test harness uses a deterministic
heuristic classifier so routing and logging can be validated offline.

Run the tests:

```bash
python run_tests.py
```

For CI or unit testing, mock `call_chat_model` in `llm_client.py` to return
stable responses for both classification and generation calls.

## Prompts & Routing

- Persona prompts are defined in `prompts.json` and loaded via `prompts.py`.
- The classifier returns an intent and confidence. If the confidence is below
	the `CONFIDENCE_THRESHOLD` (default `0.7`) the router asks a clarification
	question instead of routing to a persona.

## Logging

All routed exchanges are appended to `route_log.jsonl` as one JSON object per
line. Each entry contains at minimum:

- `timestamp` — epoch seconds
- `intent` — the routed intent (or `unclear`)
- `confidence` — classifier confidence (float)
- `user_message` — original user text
- `final_response` — assistant reply or clarification question

This format is friendly for streaming ingestion into analytics pipelines.

## Environment variables

- `OPENAI_API_KEY` — required for real LLM calls (see `.env.example`).
- `CONFIDENCE_THRESHOLD` — optional float between `0.0` and `1.0` (default `0.7`).
- `CLASSIFIER_MODEL` — override classifier model (default `gpt-3.5-turbo`).
- `RESPONSE_MODEL` — override response model (default `gpt-4o`).

## Example inputs

- `how do i sort a list of objects in python?`
- `explain this sql query`
- `This paragraph sounds awkward, can you help me fix it?`
- `I'm preparing for a job interview, any tips?`
- `what's the average of these numbers: 12, 45, 23, 67, 34`

## Contributing

Contributions are welcome. Open a GitHub issue to discuss changes or submit a
pull request with a clear description of the intent and test coverage.

---

If you'd like, I can also add a short `CONTRIBUTING.md`, expand unit tests,
or create a GitHub Actions workflow to run `run_tests.py` on each push.
