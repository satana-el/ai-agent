import os, subprocess


def run_python_file(
        working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    abs_wd = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(abs_wd, file_path))

    if not os.path.commonpath([abs_wd, target_file]) == abs_wd:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(target_file):
        return f'Error: "{file_path}" does not exist or is not a regular file'

    if not file_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file'

    command = ["python", target_file]
    if args:
        command.extend(args)

    result = subprocess.run(
        command, capture_output=True, text=True, timeout=30
    )

    output_str = ""

    if result.returncode != 0:
        output_str += f"Process exited with code {result.returncode}\n"

    if not result.stderr and not result.stdout:
        output_str += "No output produced"
    else:
        output_str += f"STDOUT: {result.stdout}\n"
        if result.stderr:
            output_str += f"STDERR: {result.stderr}"

    return output_str

