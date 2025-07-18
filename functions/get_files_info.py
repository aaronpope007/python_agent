import os

def get_files_info(working_directory, directory="."):
    full_path = os.path.join(working_directory, directory)

    full_path_abs_path = os.path.abspath(full_path)
    working_directory_abs_path = os.path.abspath(working_directory)

    common = os.path.commonpath([full_path_abs_path, working_directory_abs_path])

    if common != working_directory_abs_path:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if os.path.isdir(full_path_abs_path) is False:
        return f'Error: "{directory}" is not a directory'

    full_path_items = os.listdir(full_path_abs_path)

    formatted_file_name_strings = []

    for file in full_path_items:
        try:
            filename = os.path.join(full_path_abs_path, file)
            formatted_file_name_strings.append(f'- {file} file_size={os.path.getsize(filename)} bytes, is_dir={os.path.isdir(filename)}')
        except Exception as e:
            return f"Error: {e}"
    return "\n".join(formatted_file_name_strings)
