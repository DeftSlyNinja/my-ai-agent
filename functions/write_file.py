import os
from google import genai
from google.genai import types

def write_file(working_directory, file_path, content):
        try:
            working_dir = os.path.abspath(working_directory)
            target_path = os.path.normpath(os.path.join(working_dir, file_path))
            valid_target_path = os.path.commonpath([working_dir, target_path]) == working_dir

            if not valid_target_path:
                return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
            if os.path.isdir(target_path):
                return f'Error: Cannot write to "{file_path}" as it is a directory'
            
            parent_dir = os.path.dirname(target_path)

            os.makedirs(parent_dir, exist_ok=True)
            try:
                with open(target_path, "w") as f:
                    f.write(content)
                return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
            except Exception as e:
                return e
            
        except Exception as e:
            return f"Error: {e}"

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes to or overwrites the specified file path relative to the working directory with the provided contents.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="A string representing a file path relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="A string representing the contents to be written to the file."
            )
        },
        required=["file_path"],
    ),
)