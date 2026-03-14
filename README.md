# LLM Prompt Router

This project implements an intent-based prompt router with two main functions:

- `classify_intent(message: str)` — calls a classifier LLM to return `{intent, confidence}`.
- `route_and_respond(message: str, intent: dict)` — selects a persona prompt and produces a response.

Usage:

1. Set `OPENAI_API_KEY` in your environment (optional; code falls back to 'unclear' behavior if missing).
2. Install dependencies: `pip install -r requirements.txt`.
3. Run tests: `python run_tests.py`.

Interactive CLI
- Run the interactive CLI with:

	python app.py

- When started you'll see:

	LLM Prompt Router CLI
	Type 'exit' to quit.

- Type messages at the `User:` prompt. The CLI will show the detected intent and
	confidence, then print the generated response. Type `exit` or press Ctrl-C to quit.

Using a `.env` file
- Create a file named `.env` in the project root and add your OpenAI key:

	OPENAI_API_KEY=your_api_key_here

- The project uses `python-dotenv` to load this variable automatically. If the key
	is missing the application will print an error and classifier calls will safely
	default to `{"intent":"unclear","confidence":0.0}`.

Logs are appended to `route_log.jsonl`.

Confidence threshold safety
 - The router applies a confidence threshold to classifier outputs. If the classifier returns a confidence below the threshold the request is treated as `unclear` and the user is asked a clarification question instead of routing to an expert persona.
 - Default threshold: `0.7`. You can change it by setting the `CONFIDENCE_THRESHOLD` environment variable to a float value (e.g., `0.6`).
 - The log entries in `route_log.jsonl` include the original classifier intent and confidence as well as the final routed intent and response.

**Docker Usage**

- Build the image: `docker build -t prompt-router .`
- Run interactively with your `.env` file: `docker run -it --env-file .env prompt-router`
- Or use `docker-compose up` to build and run with the provided compose file.

**Example Inputs**

- how do i sort a list of objects in python?
- explain this sql query
- This paragraph sounds awkward
- I'm preparing for a job interview
- what's the average of these numbers: 12 45 23 67
- Help me make this better
- hey
- Can you write me a poem about clouds?
- Rewrite this sentence to be more professional
- what is a pivot table
- fix this bug: for i in range(10) print(i)
- How do I structure a cover letter?
- My boss says my writing is too verbose

**Environment Variables**

- `OPENAI_API_KEY`: your OpenAI API key (see `.env.example`)
- `CONFIDENCE_THRESHOLD`: optional float between 0.0 and 1.0 (default `0.7`)

"# LLM-Powered_Prompt" 
