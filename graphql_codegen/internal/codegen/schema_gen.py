import os
from subprocess import Popen, PIPE


def run_command(command):
    res = Popen(command, shell=True, stderr=PIPE)
    res.wait()
    try:
        stderr = res.stderr.read().decode('utf-8')
    except UnicodeDecodeError:
        stderr = res.stderr.read().decode('windows-1251')
    res.communicate()

    exit_code = res.returncode
    return exit_code, stderr


def get_schema(url, destination_path):
    command = fr'''
    python3 -m sgqlc.introspection \
    --exclude-deprecated \
    --exclude-description \
    {url} \
    {destination_path}
    '''
    return run_command(command)


def generate_schema(json_schema, destination_path):
    """
    Example:

    gen_schema(schema.json, schema.py)

    :param json_schema:
    :param destination_path:
    :return:
    """
    command = fr'''
    sgqlc-codegen schema {json_schema} {destination_path}
    '''
    return run_command(command)