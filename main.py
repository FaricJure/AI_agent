import os, sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from functions.call_function import call_function


def main():

    """response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents="Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.",
    )"""

    available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ])

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
    system_prompt = """
    You are a helpful AI coding agent. When asked to fix bugs, fix the bugs in the code without cheating or making up code that prints just the final result.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories (lists all files in a directory, used to find files to read or execute)
    - Read file contents (from a specified file, used to understand code of a file or data)
    - Execute Python files with optional arguments (to run code and get its output)
    - Write or overwrite files (to create or modify files with specified content)

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """
    model_name = "gemini-2.0-flash-001"

    max_tool_iterations = 20
    for _ in range(max_tool_iterations):
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=messages,
                config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)
            )
        except Exception as e:
            print(f"Error during generate_content: {e}", file=sys.stderr)
            break

        if verbose:
            print("Verbose mode enabled")
            print("User prompt:", user_prompt)
            if response.usage_metadata:
                print("Prompt tokens:", response.usage_metadata.prompt_token_count)
                print("Response tokens:", response.usage_metadata.candidates_token_count)
        if response.text:
            print(response.text)

        # Add the model's content back into the conversation.
        if response.candidates:
            for candidate in response.candidates:
                if candidate.content:
                    messages.append(candidate.content)

        # Determine if there are function calls.
        has_function_calls = bool(response.function_calls)
        if not has_function_calls and response.candidates:
            for candidate in response.candidates:
                if getattr(candidate, "function_calls", None):
                    has_function_calls = True
                    break

        finished = (not has_function_calls) and bool(response.text)
        if finished:
            # Final response printed above; stop looping.
            break

        # Handle any function calls.
        if has_function_calls:
            function_call_parts = []
            # Prefer top-level function_calls; fall back to per-candidate.
            function_calls_to_run = response.function_calls or []
            if not function_calls_to_run and response.candidates:
                for candidate in response.candidates:
                    if getattr(candidate, "function_calls", None):
                        function_calls_to_run.extend(candidate.function_calls)

            for function_call_part in function_calls_to_run:
                print(f"Calling function: {function_call_part.name}({function_call_part.args})")
                function_call_result = call_function(function_call_part, verbose=verbose)
                if not (
                    function_call_result.parts
                    and function_call_result.parts[0].function_response
                    and function_call_result.parts[0].function_response.response
                ):
                    raise RuntimeError("Function call result missing function_response")
                function_call_parts.append(function_call_result.parts[0])
                if verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")

            # Append tool responses as a new user message for the next turn.
            messages.append(types.Content(role="user", parts=function_call_parts))
            # Continue loop to let the model respond to tool outputs.
            continue

        # If no function calls and not finished (e.g., empty text), continue until max iterations.
        continue


if __name__ == "__main__":
    main()
