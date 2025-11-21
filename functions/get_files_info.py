import os


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
