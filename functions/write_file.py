import os

def write_file(working_directory, file_path, content):
    try:
        abs_path = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(abs_path, file_path))
        valid_target = os.path.commonpath([abs_path, target_file_path]) == abs_path
    except Exception as e:
        return f"Error: {e}"
    
    if not valid_target:
        return f'\tError: Cannot write to "{file_path}" as it is outside the permitted working directory'
    if  os.path.isdir(target_file_path):
        return f'Error: Cannot write to "{file_path}" as it is a directory'
    
    os.makedirs(os.path.dirname(target_file_path), exist_ok=True)
    
    with open(target_file_path, "w") as f:
        if f.write(content) == len(content):
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    return f'Error: Failed to write all content to "{file_path}"'
        