from google.genai import types
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.run_python_file import run_python_file
from functions.write_file import write_file


def call_function(function_call_part, verbose=False):
    function_name = function_call_part.name
    function_args = function_call_part.args or {}
    function_result = None

    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    working_directory = "./calculator"  # Example working directory

    if function_name == "get_files_info":
        directory = function_args.get("directory", ".")
        function_result = get_files_info(working_directory, directory)
    elif function_name == "get_file_content":
        file_path = function_args.get("file_path")
        function_result = get_file_content(working_directory, file_path)
    elif function_name == "run_python_file":
        file_path = function_args.get("file_path")
        args = function_args.get("args", [])
        function_result = run_python_file(working_directory, file_path, args)
    elif function_name == "write_file":
        file_path = function_args.get("file_path")
        content = function_args.get("content", "")
        function_result = write_file(working_directory, file_path, content)
    else:
        function_result = f"Unknown function: {function_name}"

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )
