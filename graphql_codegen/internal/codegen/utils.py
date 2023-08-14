from pathlib import Path
from subprocess import Popen, PIPE
from graphql_codegen import logger


def write_code_to_file(file_path, content):
    logger.info(f'write code to file: {file_path}')
    Path(file_path).write_text(content)


def create_directory(output):
    logger.info(f'Create directory: {output}')
    directory = Path(output)
    directory.mkdir(exist_ok=True)
    directory.joinpath('__init__.py').touch()
    return directory


def run_command(command):
    logger.info(f'Run command: {command}')
    res = Popen(command, shell=True, stderr=PIPE)
    res.wait()
    try:
        stderr = res.stderr.read().decode('utf-8')
    except UnicodeDecodeError:
        stderr = res.stderr.read().decode('windows-1251')
    res.communicate()

    exit_code = res.returncode
    logger.info(f'Result: {exit_code}, {stderr}')
    return exit_code, stderr
