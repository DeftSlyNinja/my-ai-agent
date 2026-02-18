import os
from google import genai
from google.genai import types

def get_file_content(working_directory, file_path):
    try:
        working_dir = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(working_dir, file_path))
        valid_target_path = os.path.commonpath([working_dir, target_path]) == working_dir

        if not valid_target_path:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        MAX_CHARS = 10000
        with open(target_path, 'r') as f:
            contents = f.read(MAX_CHARS)
            if f.read(1):
                contents += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            return contents
    except Exception as e:
        return f"Error: {e}"

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Returns the contents of a file at a specified file path relative to the working directory. Truncates at 10000 characters.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="A string representing a file path relative to the working directory.",
            ),
        },
        required=["file_path"],
    ),
)