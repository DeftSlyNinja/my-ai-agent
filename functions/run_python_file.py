import os
import subprocess

def run_python_file(working_directory, file_path, args=None):
    try:
        working_dir = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(working_dir, file_path))
        valid_target_path = os.path.commonpath([working_dir, target_path]) == working_dir
        if not valid_target_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        
        if not target_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'
        
        command = ["python", target_path]
        if args != None:
            command.extend(args)
        result = subprocess.run(command, capture_output=True, cwd=working_directory, timeout=30, text=True)

        output_str = ""
        if result.returncode != 0:
            output_str += f"Process exited with code {result.returncode}"
        if result.stderr == "" and result.stdout == "":
            output_str += "\nNo output produced"
        else:
            output_str+= f"\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}"
        return output_str
    except Exception as e:
        return f"Error: executing Python file: {e}"
