import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes files.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to write, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write into the file.",
            ),
        },
    ),
)

def write_file(working_directory, file_path, content):

    full_file_path = os.path.join(working_directory, file_path)

    working_directory_real_path = os.path.realpath(working_directory)

    if not working_directory_real_path.endswith(os.path.sep):
        working_directory_real_path += os.path.sep

    file_path_real_path = os.path.realpath(full_file_path)

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
