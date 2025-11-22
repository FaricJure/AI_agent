from google.genai import types


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Returns the content of a specified file within the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to read, relative to the working directory.",
            ),
        },
    ),
)

def get_file_content(working_directory, file_path):
    """Return the content of a file within the working directory."""
    import os

    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file_abs = os.path.abspath(os.path.join(working_dir_abs, file_path))

        # Ensure target file stays within the working directory bounds.
        if not target_file_abs.startswith(working_dir_abs + os.sep):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_file_abs):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(target_file_abs, "r") as file:
            content = file.read()
            if len(content) > 10000:
                return content[:10000], f'[...File "{file_path}" truncated at 10000 characters]'
            else:
                return content
            
    except Exception as e:
        return f"Error: {e}"