import os
from google.genai import types


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

def get_files_info(working_directory, directory="."):
    """Return a formatted listing of files within the working directory."""
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir_abs = os.path.abspath(os.path.join(working_dir_abs, directory))

        # Ensure target directory stays within the working directory bounds.
        if not (
            target_dir_abs == working_dir_abs
            or target_dir_abs.startswith(working_dir_abs + os.sep)
        ):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(target_dir_abs):
            return f'Error: "{directory}" is not a directory'

        entries = []
        for entry in sorted(os.listdir(target_dir_abs)):
            entry_path = os.path.join(target_dir_abs, entry)
            try:
                size = os.path.getsize(entry_path)
                is_dir = os.path.isdir(entry_path)
                entries.append(f"- {entry}: file_size={size} bytes, is_dir={is_dir}")
            except OSError as e:
                return f"Error: {e}"

        return "\n".join(entries)
    except Exception as e:
        return f"Error: {e}"
