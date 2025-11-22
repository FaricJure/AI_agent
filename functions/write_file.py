import google.genai.types as types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a specified file within the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to write to, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write into the file.",
            ),
        },
    ),
)

def write_file(working_directory, file_path, content):
    """Write content to a file within the working directory."""
    import os

    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file_abs = os.path.abspath(os.path.join(working_dir_abs, file_path))

        # Ensure target file stays within the working directory bounds.
        if not target_file_abs.startswith(working_dir_abs + os.sep):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        # Create parent directories if they do not exist.
        os.makedirs(os.path.dirname(target_file_abs), exist_ok=True)

        with open(target_file_abs, "w") as file:
            file.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {e}"