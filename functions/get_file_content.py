import os
from config import MAX_CHARS

def get_file_content(working_directory: str, file_path: str) -> str:
    abs_wd = os.path.abspath(working_directory)
    target_file = os.path.join(abs_wd, file_path)

    if not os.path.commonpath([abs_wd, target_file]) == abs_wd:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(target_file):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    with open(target_file, "r") as f:
        file_content_string = f.read(MAX_CHARS)
        if f.read(1):
            file_content_string +=  f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
    return file_content_string

schema_get_file_content= {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Reads and retruns the contents of a file relative to the working directory.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the files to read contents from, relative to the working directory (default is the working directory itself)",
                },
            },
            "required": ["file_path"],
        },
    },
}
