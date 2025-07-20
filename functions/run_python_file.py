import os
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs python file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the Python file to execute, relative to the working directory.",
            ),
        },
    ),
)

def run_python_file(working_directory, file_path, args=[]):
    full_file_path = os.path.join(working_directory, file_path)

    working_directory_real_path = os.path.realpath(working_directory)

    if not working_directory_real_path.endswith(os.path.sep):
        working_directory_real_path += os.path.sep

    file_path_real_path = os.path.realpath(full_file_path)
    file_path_in_working_dir = file_path_real_path.startswith(working_directory_real_path)

    if file_path_in_working_dir == False:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(full_file_path):
        return f'Error: File "{file_path}" not found.'

    if not full_file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'


    command = ["python", os.path.basename(file_path)] + args



    try:
        completed_process = subprocess.run(
            command,                                      # The command and its arguments as a list
            capture_output=True,                          # This captures both stdout and stderr
            text=True,                                    # This returns output as a string instead of bytes
            cwd=working_directory_real_path,                        # Run command in a particular working directory
            timeout=30                                    # Abort if still running after 30 seconds
        )
        if not completed_process.stdout and not completed_process.stderr:
            return "No output produced."
        result = f"STDOUT:{completed_process.stdout.rstrip()}\nSTDERR:{completed_process.stderr.rstrip()}"
        if completed_process.returncode != 0:
            result += f"\nProcess exited with code {completed_process.returncode}"
        return result
    except Exception as e:
        return f"Error: executing Python file: {e}"
