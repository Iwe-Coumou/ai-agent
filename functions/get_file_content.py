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
            