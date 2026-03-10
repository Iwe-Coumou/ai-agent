import os
import subprocess

def run_python_file(working_directory, file_path, args=None):
    try:
        abs_path = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(abs_path, file_path))
        valid_target = os.path.commonpath([abs_path, target_file_path]) == abs_path
    except Exception as e:
        return f"Error: {e}"
    
    if not valid_target:
        return f'\tError: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if  not (os.path.exists(target_file_path) and os.path.isfile(target_file_path)):
        return f'\tError: "{file_path}" does not exist or is not a regular file'
    if not file_path.endswith(".py"):
        return f'\tError: "{file_path}" is not a Python file'
    
    command = ["python", target_file_path]
    if args:
        command.extend(args)
        
    try:
        result = subprocess.run(command, text=True, capture_output=True, timeout=30.0, cwd=working_directory)
    except subprocess.TimeoutExpired:
        return f'\tError: "{file_path}" timed out'
    except Exception as e:
        return f"\tError: {e}"
        
    output = ""
    if result.returncode != 0:
        output += f"Process exited with code {result.returncode}\n"
    if not (result.stdout or result.stderr):
        output += f"No output produced\n"
    else:
        output += f"STDOUT:\n{result.stdout}"
        output += f"STDERR: \n{result.stderr}"
    
    return output
    
from google.genai import types

schema_run_python = types.FunctionDeclaration(
    name="run_python",
    description="Runs the python script specified by filepath (relative from working directory) with the given arguments",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to the desired python file, relative to the working directory (default is the working directory itself)",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="A list of the arguments to give to the function"
            )
        },
    ),
    required=["file_path"]
)