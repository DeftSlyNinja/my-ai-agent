import os

def get_files_info(working_directory, directory="."):
    try:
        working_dir = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir, directory))
        valid_target_dir = os.path.commonpath([working_dir, target_dir]) == working_dir

        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'
        
        files = os.listdir(target_dir)
        fstring_list = []
        for item in files:
            newpath = f"{target_dir}/{item}"
            file_string = f" - {item}: file_size={os.path.getsize(newpath)} bytes, is_dir={os.path.isdir(newpath)}"
            fstring_list.append(file_string)
        combined_string = '\n'.join(fstring_list)
        return combined_string
    except Exception as e:
        return f"Error: {e}"