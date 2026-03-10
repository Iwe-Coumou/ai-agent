import os
from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    try:
        abs_path = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(abs_path, file_path))
        valid_target = os.path.commonpath([abs_path, target_path]) == abs_path
    except Exception as e:
        return f"Error: {e}"
    
    if not valid_target:
        return f'\tError: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target_path):
        return f"\tError: File not found or is not a regular file: {file_path}"
    
    with open(target_path, "r") as f:
        content = f.read(MAX_CHARS)
        if f.read(1):
            content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            
    return content

from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Returns a string of the file's contents with a max of 10000 characters, if the file was larger there will be a truncation indication at the end of the string",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to the desired file, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
    required=["file_path"]
)
            