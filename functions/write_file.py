import os

def write_file(working_directory, file_path, content):

    working_directory_real_path = os.path.realpath(working_directory)
    file_path_real_path = os.path.realpath(file_path)

    file_path_in_working_dir = file_path_real_path.startswith(working_directory_real_path)

    if file_path_in_working_dir == False:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    os.makedirs(os.path.dirname(file_path_real_path), exist_ok=True)

    try:
        with open(file_path_real_path, "w") as f:
            f.write(content)
    except Exception as e:
        return f"Error: {e}"

    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
