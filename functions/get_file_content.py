import os
import config

def get_file_content(working_directory, file_path=""):

    full_path = os.path.join(working_directory, file_path)
    full_path_abs_path = os.path.abspath(full_path)

    working_directory_abs_path = os.path.abspath(working_directory)

    common = os.path.commonpath([full_path_abs_path, working_directory_abs_path])

    if common != working_directory_abs_path:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if os.path.isfile(full_path_abs_path) is False:
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        with open(full_path_abs_path) as file:
            content = file.read(config.MAX_CHARS + 1)
            if len(content) > config.MAX_CHARS:
                return content[:config.MAX_CHARS] + f' [...File "{file_path}" truncated at {config.MAX_CHARS} characters]'
            else:
                return content
    except Exception as e:
        return f"Error: {e}"
