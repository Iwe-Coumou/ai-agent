import os

def get_files_info(working_directory, directory="."):
    try:
        abs_path = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(abs_path, directory))
        valid_target = os.path.commonpath([abs_path, target_dir]) == abs_path
    except Exception as e:
        return f"Error: {e}"
    
    if not valid_target:
        return f'\tError: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(target_dir):
        return f'Error: "{directory}" is not a directory'
    
    dir_log = []
    for name in os.listdir(target_dir):
        try:
            file_path = os.path.join(target_dir, name)
            file_size = os.path.getsize(file_path)
            is_dir = os.path.isdir(file_path)
        except Exception as e:
            return f"\tError: {e}"
        
        dir_log.append((name, file_size, is_dir))
    
    return "\n".join(map(lambda item: f"\t- {item[0]}: file_size= {item[1]} bytes, is_dir={item[2]}" , dir_log))