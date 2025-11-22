import google.genai.types as types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file within the working directory and returns its output.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the Python file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                ),
                description="A list of command-line arguments to pass to the Python file.",
            ),
        },
    ),
)


def run_python_file(working_directory, file_path, args=None):
    """Run a Python file within the working directory and return its output."""
    import os
    import subprocess

    try:
        args = args or []
        working_dir_abs = os.path.abspath(working_directory)
        target_file_abs = os.path.abspath(os.path.join(working_dir_abs, file_path))

        # Ensure target file stays within the working directory bounds.
        if not target_file_abs.startswith(working_dir_abs + os.sep):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_file_abs):
            return f'Error: File "{file_path}" not found.'

        if not target_file_abs.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'

        # Construct the command to run the Python file.
        command = ["python", target_file_abs] + list(args)

        # Run the command and capture output.
        result = subprocess.run(
            command,
            cwd=working_dir_abs,
            capture_output=True,
            text=True,
            timeout=30,  # Prevent long-running processes
        )

        stdout = result.stdout or ""
        stderr = result.stderr or ""

        output_parts = []
        if stdout:
            output_parts.append(f"STDOUT:\n{stdout}".rstrip())
        if stderr:
            output_parts.append(f"STDERR:\n{stderr}".rstrip())
        if result.returncode != 0:
            output_parts.append(f"Process exited with code {result.returncode}")

        if not output_parts:
            return "No output produced."

        return "\n".join(output_parts)

    except subprocess.TimeoutExpired:
        return "Error: Execution timed out"
    except Exception as e:
        return f"Error: executing Python file: {e}"
