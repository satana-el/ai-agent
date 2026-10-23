import os


def write_file(working_directory: str, file_path: str, content: str) -> str:
    abs_wd = os.path.abspath(working_directory)
    target_file = os.path.join(abs_wd, file_path)

    if not os.path.commonpath([abs_wd, target_file]) == abs_wd:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    if os.path.isdir(target_file):
        return f'Error: Cannot write to "{file_path}" as it is a directory'

    try:
        os.makedirs(os.path.commonpath([abs_wd, target_file]), exist_ok=True)
    except FileExistsError:
        pass

    with open(target_file, "w") as f:
        f.write(content)

    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
