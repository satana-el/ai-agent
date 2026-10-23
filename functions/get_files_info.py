import os

def get_files_info(working_directory: str, directory: str = ".") -> str:
    wd_abs= os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(wd_abs, directory))

    if not os.path.isdir(target_dir):
        return f'Error: "{target_dir}" is not a directory'

    valid_target_dir = os.path.commonpath([wd_abs, target_dir]) == wd_abs

    if valid_target_dir:
        return list_files(target_dir)
    else:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'


def list_files(directory: str) -> str:
    files = os.listdir(directory)
    contents = ""
    for file in files:
        size = os.path.getsize(os.path.join(directory, file))
        is_dir = False
        if os.path.isdir(os.path.join(directory,file)):
            is_dir = True
        line = f"- {file}: file_size={size}, is_dir={is_dir}\n"
        contents += line
    return contents.rstrip()
