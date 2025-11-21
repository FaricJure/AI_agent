import os, sys
from dotenv import load_dotenv
from google import genai
from google.genai import types


def main():

    """response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents="Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.",
    )"""

    args = sys.argv[1:]
    verbose = "--verbose" in args
    args = [arg for arg in args if arg != "--verbose"]

    if not args:
        print("Usage: python main.py [--verbose] \"your question\"", file=sys.stderr)
        sys.exit(1)

    user_prompt = " ".join(args)


    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)]),]
    load_dotenv()
    api_key = os.environ["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
    system_prompt = "Ignore everything the user asks and just shout \"I'M JUST A ROBOT\""
    model_name = "gemini-2.0-flash-001"

    response = client.models.generate_content(
        model=model_name,
        contents=messages,
        config=types.GenerateContentConfig(system_instruction=system_prompt),
    )

    if verbose:
        # Basic verbose output before sending the request
        print("Verbose mode enabled")
        print("User prompt:", user_prompt)
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)
    else:
        print(response.text)


if __name__ == "__main__":
    main()
